"""Render a storyboard into a portable Rev D edit-review board."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def tc(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--out")
    args = ap.parse_args()
    source = Path(args.storyboard)
    data = json.loads(source.read_text())
    out = Path(args.out) if args.out else source.with_name("storyboard_review.html")
    cards = []
    for index, screen in enumerate(data["screens"], 1):
        intent = html.escape(screen.get("visual_intent") or "")
        query = html.escape(screen.get("search_query") or "")
        title = html.escape(screen.get("heading") or screen["id"])
        reveal = html.escape((screen.get("reveals") or [{}])[0].get("title") or "")
        blocker = screen["layout"] in {"broll", "screen_rec"} and not query
        cards.append(f'''<article class="beat state-{screen.get('narrative_state','build')}" data-state="{screen.get('narrative_state','')}" data-role="{screen.get('footage_role','')}" data-layout="{screen['layout']}">
          <div class="frame"><span class="index">{index:02d}</span><span class="layout">{screen['layout'].replace('_',' ')}</span><strong>{reveal or title}</strong><i>{screen.get('camera','system')} camera</i></div>
          <div class="meta"><div class="time">{tc(screen['start'])}–{tc(screen['end'])}<small>{screen['end']-screen['start']:.1f}s</small></div><div><h2>{title}</h2><p>{intent}</p>{f'<code>{query}</code>' if query else ''}</div></div>
          <footer><span>{screen.get('narrative_state','')}</span><span>{screen.get('footage_role','')}</span><span>score · {screen.get('score_state','')}</span>{'<b>MEDIA BRIEF NEEDED</b>' if blocker else ''}</footer>
        </article>''')
    states = " → ".join(data.get("narrative_waveform", []))
    document = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EP006 · Rev D Storyboard</title><style>
    :root{{--paper:#f5f0e6;--ink:#171717;--navy:#14263e;--gold:#b78b2d;--brick:#9e4439;--cobalt:#1769e0;--line:#d8d0c2;--muted:#68645d}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.45 "Helvetica Neue",Helvetica,sans-serif}}header{{position:sticky;top:0;z-index:5;background:rgba(245,240,230,.94);backdrop-filter:blur(14px);border-bottom:1px solid var(--line);padding:28px 4vw 20px}}.brand{{font-weight:900;letter-spacing:-.045em;font-size:clamp(30px,4vw,62px);line-height:.9}}.eyebrow,.layout,footer,button{{font:700 11px/1.2 ui-monospace,SFMono-Regular,monospace;text-transform:uppercase;letter-spacing:.12em}}.wave{{color:var(--gold);margin-top:13px}}nav{{display:flex;gap:7px;flex-wrap:wrap;margin-top:18px}}button{{border:1px solid var(--line);background:transparent;border-radius:99px;padding:8px 12px;cursor:pointer}}button.active{{background:var(--ink);color:var(--paper)}}main{{padding:34px 4vw 100px;display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:22px}}.beat{{border:1px solid var(--line);background:#fffaf0;box-shadow:0 12px 36px rgba(20,38,62,.06);transition:.2s transform,.2s opacity}}.beat:hover{{transform:translateY(-4px)}}.frame{{height:210px;background:var(--navy);color:white;padding:24px;position:relative;display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden}}.frame:before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(90deg,transparent 0 39px,rgba(255,255,255,.035) 40px),repeating-linear-gradient(0deg,transparent 0 39px,rgba(255,255,255,.035) 40px)}}.frame strong{{position:relative;font-size:27px;line-height:1.02;letter-spacing:-.035em;max-width:85%}}.frame i{{position:relative;color:#bfc8d2;margin-top:10px;font:12px ui-monospace,monospace}}.index{{position:absolute;top:20px;left:22px;font:800 42px ui-monospace,monospace;color:rgba(255,255,255,.14)}}.layout{{position:absolute;top:22px;right:22px;color:#e2bb64}}.state-peril .frame{{background:linear-gradient(145deg,#16263d,#0e1724)}}.state-absurdity .frame{{background:linear-gradient(145deg,#17345b,var(--cobalt))}}.state-reversal .frame{{background:linear-gradient(145deg,#5a281f,var(--brick))}}.state-build .frame{{background:linear-gradient(145deg,#14263e,#25445e)}}.state-agency .frame{{background:linear-gradient(145deg,#5b4516,var(--gold))}}.meta{{display:grid;grid-template-columns:68px 1fr;gap:18px;padding:22px}}.time{{font:800 15px ui-monospace,monospace}}.time small{{display:block;color:var(--muted);font-weight:500;margin-top:4px}}h2{{font-size:17px;margin:0 0 8px}}p{{color:#48453f;margin:0 0 12px}}code{{display:block;background:#eee7d9;padding:9px 10px;font-size:11px;white-space:normal}}footer{{display:flex;gap:7px;flex-wrap:wrap;padding:0 22px 20px;color:var(--muted)}}footer span,footer b{{border:1px solid var(--line);padding:6px 8px}}footer b{{color:var(--brick);border-color:var(--brick)}}.hidden{{display:none}}@media(max-width:620px){{main{{grid-template-columns:1fr;padding-inline:16px}}header{{padding-inline:16px}}}}
    </style></head><body><header><div class="eyebrow">Operator Blueprint · № 006 · Edit board</div><div class="brand">Hotels Pay 30% to Book Their Own Rooms</div><div class="wave">{html.escape(states)}</div><nav><button class="active" data-filter="all">All 46 beats</button><button data-filter="human_context">Human</button><button data-filter="proof">Proof</button><button data-filter="process">Process</button><button data-filter="outcome">Outcome</button><button data-filter="broll">B-roll</button><button data-filter="screen_rec">Screen capture</button></nav></header><main>{''.join(cards)}</main><script>
    const cards=[...document.querySelectorAll('.beat')];document.querySelectorAll('button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('button').forEach(x=>x.classList.remove('active'));b.classList.add('active');const f=b.dataset.filter;cards.forEach(c=>c.classList.toggle('hidden',f!=='all'&&c.dataset.role!==f&&c.dataset.layout!==f));}});
    </script></body></html>'''
    out.write_text(document)
    print(f"Storyboard review → {out}")


if __name__ == "__main__":
    main()
