"""Render a storyboard into a portable, script-aligned edit-review board."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def tc(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def spoken_text(words: list[dict], start: float, end: float) -> str:
    selected = [
        str(word.get("word", "")).strip()
        for word in words
        if float(word.get("start", 0)) < end and float(word.get("end", 0)) > start
    ]
    return " ".join(word for word in selected if word)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--out")
    ap.add_argument("--words", help="Word-timing JSON; defaults to vo/words.json")
    ap.add_argument("--frames", help="Directory containing rendered storyboard JPGs")
    args = ap.parse_args()
    source = Path(args.storyboard)
    data = json.loads(source.read_text())
    out = Path(args.out) if args.out else source.with_name("storyboard_review.html")
    words_path = Path(args.words) if args.words else source.parent / "vo" / "words.json"
    words = json.loads(words_path.read_text()) if words_path.exists() else []
    frames_dir = Path(args.frames) if args.frames else source.parent / "storyboard_frames"
    cards = []

    for index, screen in enumerate(data["screens"], 1):
        intent = html.escape(screen.get("visual_intent") or "")
        query = html.escape(screen.get("search_query") or "")
        title = html.escape(screen.get("heading") or screen["id"])
        blocker = screen["layout"] in {"broll", "screen_rec"} and not query
        narration = html.escape(spoken_text(words, screen["start"], screen["end"]))
        frame_name = f"{index:02d}-{screen['id']}.jpg"
        frame_path = frames_dir / frame_name
        try:
            frame_src = frame_path.relative_to(out.parent).as_posix()
        except ValueError:
            frame_src = frame_path.resolve().as_uri()
        visual = (
            f'<img src="{html.escape(frame_src)}" alt="Rendered frame for {title}">'
            if frame_path.exists()
            else f'<div class="missing">Render frame missing<br><code>{html.escape(frame_name)}</code></div>'
        )
        cards.append(f'''<article class="beat" data-role="{screen.get('footage_role','')}" data-layout="{screen['layout']}">
          <div class="frame">{visual}<span class="index">{index:02d}</span><span class="layout">{screen['layout'].replace('_',' ')}</span></div>
          <div class="meta"><div class="time">{tc(screen['start'])}–{tc(screen['end'])}<small>{screen['end']-screen['start']:.1f}s</small></div><div><h2>{title}</h2><h3>Voiceover</h3><blockquote>{narration or 'No narration in this interval.'}</blockquote><h3>Visual job</h3><p>{intent}</p>{f'<code>{query}</code>' if query else ''}</div></div>
          <footer><span>{screen.get('narrative_state','')}</span><span>{screen.get('footage_role','')}</span><span>score · {screen.get('score_state','')}</span>{'<b>MEDIA BRIEF NEEDED</b>' if blocker else ''}</footer>
        </article>''')
        if screen["id"] == "hook-04":
            ident_start, ident_end = 24.209, 28.209
            ident_vo = html.escape(spoken_text(words, ident_start, ident_end))
            logo = frames_dir / "00a-ident-logo.jpg"
            title_card = frames_dir / "00b-ident-title.jpg"
            def relative_image(path: Path, label: str) -> str:
                try:
                    src = path.relative_to(out.parent).as_posix()
                except ValueError:
                    src = path.resolve().as_uri()
                return f'<img src="{html.escape(src)}" alt="{label}">' if path.exists() else f'<div class="missing">{label} frame missing</div>'
            cards.append(f'''<article class="beat ident" data-role="identity" data-layout="ident">
              <div class="ident-grid"><div class="frame">{relative_image(logo, 'Operator Economy logo ident')}<span class="layout">logo · 2.4s</span></div><div class="frame">{relative_image(title_card, 'Episode title ident')}<span class="layout">title · 1.6s</span></div></div>
              <div class="meta"><div class="time">00:24–00:28<small>4.0s overlay</small></div><div><h2>Logo sting → episode title</h2><h3>Voiceover beneath ident</h3><blockquote>{ident_vo or 'This is The Operator Economy. This week: direct booking recovery.'}</blockquote><h3>Visual job</h3><p>Reset after the cold open, establish the series, then name the episode without breaking narration momentum.</p></div></div>
              <footer><span>identity</span><span>logo + title</span><span>sting · oe-sting-rev-e-soft</span></footer>
            </article>''')

    states = " → ".join(data.get("narrative_waveform", []))
    document = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EP006 · Script-aligned storyboard</title><style>
    :root{{--paper:#f5f0e6;--ink:#171717;--navy:#14263e;--gold:#b78b2d;--brick:#9e4439;--line:#d8d0c2;--muted:#68645d}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.45 "Helvetica Neue",Helvetica,sans-serif}}header{{position:sticky;top:0;z-index:5;background:rgba(245,240,230,.94);backdrop-filter:blur(14px);border-bottom:1px solid var(--line);padding:24px 4vw 18px}}.brand{{font-weight:900;letter-spacing:-.045em;font-size:clamp(30px,4vw,58px);line-height:.9}}.eyebrow,.layout,footer,button,h3{{font:700 11px/1.2 ui-monospace,SFMono-Regular,monospace;text-transform:uppercase;letter-spacing:.12em}}.wave{{color:var(--gold);margin-top:12px}}.summary{{color:var(--muted);margin-top:7px}}nav{{display:flex;gap:7px;flex-wrap:wrap;margin-top:14px}}button{{border:1px solid var(--line);background:transparent;border-radius:99px;padding:8px 12px;cursor:pointer}}button.active{{background:var(--ink);color:var(--paper)}}main{{padding:34px 4vw 100px;display:grid;grid-template-columns:repeat(auto-fit,minmax(440px,1fr));gap:26px}}.beat{{border:1px solid var(--line);background:#fffaf0;box-shadow:0 12px 36px rgba(20,38,62,.06);transition:.2s transform,.2s opacity;overflow:hidden}}.beat:hover{{transform:translateY(-3px)}}.ident{{grid-column:1/-1;border:2px solid var(--gold)}}.ident-grid{{display:grid;grid-template-columns:1fr 1fr}}.frame{{aspect-ratio:16/9;background:var(--navy);color:white;position:relative;overflow:hidden}}.frame img{{display:block;width:100%;height:100%;object-fit:cover}}.missing{{height:100%;display:grid;place-content:center;text-align:center;color:#fff}}.index{{position:absolute;top:14px;left:16px;font:800 28px ui-monospace,monospace;color:white;background:rgba(10,16,24,.78);padding:6px 9px;border-radius:4px}}.layout{{position:absolute;top:16px;right:16px;color:#f1d38d;background:rgba(10,16,24,.78);padding:7px 9px;border-radius:4px}}.meta{{display:grid;grid-template-columns:76px 1fr;gap:20px;padding:24px}}.time{{font:800 15px ui-monospace,monospace}}.time small{{display:block;color:var(--muted);font-weight:500;margin-top:4px}}h2{{font-size:20px;line-height:1.15;margin:0 0 18px}}h3{{margin:16px 0 7px;color:var(--muted)}}blockquote{{margin:0;border-left:4px solid var(--gold);padding:2px 0 2px 14px;font-size:17px;line-height:1.5;font-weight:600}}p{{color:#48453f;margin:0 0 12px}}code{{display:block;background:#eee7d9;padding:9px 10px;font-size:11px;white-space:normal}}footer{{display:flex;gap:7px;flex-wrap:wrap;padding:0 24px 22px;color:var(--muted)}}footer span,footer b{{border:1px solid var(--line);padding:6px 8px}}footer b{{color:var(--brick);border-color:var(--brick)}}.hidden{{display:none}}@media(max-width:620px){{main{{grid-template-columns:1fr;padding-inline:14px}}header{{padding-inline:16px}}.meta{{grid-template-columns:1fr}}.ident-grid{{grid-template-columns:1fr}}}}
    </style></head><body><header><div class="eyebrow">Operator Blueprint · № 011 · Script-aligned edit board</div><div class="brand">Hotels Keep Paying to Meet the Same Guest</div><div class="wave">{html.escape(states)}</div><div class="summary">31 authored screens · exact timed VO · actual Remotion frames · ident overlays at 00:24–00:28</div><nav><button class="active" data-filter="all">All {len(data['screens'])} screens</button><button data-filter="human_context">Human</button><button data-filter="proof">Proof</button><button data-filter="process">Process</button><button data-filter="outcome">Outcome</button><button data-filter="broll">B-roll</button><button data-filter="screen_rec">Screen capture</button></nav></header><main>{''.join(cards)}</main><script>
    const cards=[...document.querySelectorAll('.beat')];document.querySelectorAll('button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('button').forEach(x=>x.classList.remove('active'));b.classList.add('active');const f=b.dataset.filter;cards.forEach(c=>c.classList.toggle('hidden',f!=='all'&&c.dataset.role!==f&&c.dataset.layout!==f));}});
    </script></body></html>'''
    out.write_text(document)
    print(f"Storyboard review → {out}")


if __name__ == "__main__":
    main()
