#!/usr/bin/env python3
"""Build the single private review page for EP009 SHORTS-004.

Same private host layout the r3 review used, so the existing review server picks
it up: blueprint-cinema/experiments/EP009-FULL-BUILD-001/assembly/qa/ep009-shorts-r4/.
Videos are symlinked, never copied. Nothing is uploaded or published.
"""
from pathlib import Path
import html
import json
import os
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oe_shorts_r4 as L  # noqa: E402

P = Path(__file__).resolve().parent
QA = L.FULL / "assembly/qa/ep009-shorts-r4"
ORDER = ["01-second-commission", "04-wrong-number", "02-cheap-tools", "03-guest-relationship"]

RECUT = {
    "01-second-commission":
        "Re-cut: the proof beat extended one sentence to master f948 so the payoff finishes "
        "out loud. End card now states the fact instead of asking what the inn can pay. "
        "Presenter share of speech drops 0.665 to 0.516.",
    "04-wrong-number":
        "Not re-cut. Both beats keep their r3 frames. End card now states the cap, and the "
        "constraint beat finally carries an overlay.",
    "02-cheap-tools":
        "Re-cut: a presenter orientation beat added in front (master f1687 to f1842) so the "
        "Short says small hotel, returning guests, direct booking and booking site out loud. "
        "Presenter share of speech rises 0.668 to 0.765.",
    "03-guest-relationship":
        "Re-cut per your ruling: extended to master f4890 so the answer is spoken, and the "
        "end card that repeated the question is gone. The answer beat has no presenter "
        "picture and is carried by a card.",
}
WEAKNESS = {
    "01-second-commission":
        "The proof insert is now the longest beat at 7.0 s, which is a real trade against "
        "avatar-forward. Return it if you want the presenter share back.",
    "04-wrong-number":
        "“It’s the wrong number” only has a referent because the design puts the number "
        "in frame one. The speech alone never says small hotel.",
    "02-cheap-tools":
        "The new opening still starts on an unresolved pronoun, “It helps a small hotel”. "
        "The on-screen line supplies the referent; the locked narration has no better in point.",
    "03-guest-relationship":
        "The presenter picture ends 1.9 s before the speech does. seg019 coverage stops at "
        "frame 4844, so the spoken answer runs under a card, not a face.",
}

CSS = """*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:#F5F0E6;color:#173530;font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{max-width:1180px;margin:auto;padding:40px 22px 90px}
header{max-width:820px;margin-bottom:34px}
.eyebrow{font-size:12px;letter-spacing:.14em;font-weight:700;color:#586D74}
h1{font:600 clamp(36px,6.4vw,62px)/1.03 Georgia,serif;letter-spacing:-.04em;margin:18px 0}
header p{font-size:18px;max-width:700px}
.tip{padding-left:15px;border-left:3px solid #B5482F}
nav{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}
nav a{color:inherit;text-decoration:none;border:1px solid #C4B99E;padding:10px 15px;border-radius:4px;background:#FBF8F1}
nav a:hover{border-color:#B5482F}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px}
.card{background:#FBF8F1;border:1px solid #D8CFB9;padding:18px;border-radius:8px;scroll-margin-top:20px}
.meta{display:flex;justify-content:space-between;color:#586D74;font-size:12px;letter-spacing:.07em}
h2{font:600 27px/1.14 Georgia,serif;letter-spacing:-.025em;margin:13px 0 16px}
video{display:block;width:100%;aspect-ratio:9/16;object-fit:contain;background:#111713;border-radius:3px}
.notes{font-size:14px;line-height:1.5}
.notes section{margin:18px 0}
.notes b{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.09em;color:#586D74;margin-bottom:5px}
.spoken{font-style:italic}
pre{white-space:pre-wrap;font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;background:#F1EADA;border:1px solid #DED4BE;padding:12px;border-radius:4px;margin:0}
.ruling{margin-top:18px;padding-top:16px;border-top:1px solid #DED4BE}
.ruling label{display:inline-flex;align-items:center;gap:7px;margin-right:16px;font-size:14px}
.ruling textarea{width:100%;margin-top:10px;min-height:54px;font:14px/1.45 inherit;padding:8px;border:1px solid #C4B99E;border-radius:4px;background:#FFFDF8;color:inherit}
.bar{position:sticky;bottom:0;background:#173530;color:#F5F0E6;padding:14px 18px;border-radius:8px;margin-top:30px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.bar button{font:600 15px inherit;padding:11px 16px;border:0;border-radius:4px;background:#F5F0E6;color:#173530;cursor:pointer}
.bar span{font-size:14px}
a{color:#A3422C}
footer{margin-top:32px;max-width:820px;font-size:13px;color:#586D74}
@media(max-width:760px){main{padding:26px 16px 60px}.grid{grid-template-columns:1fr}.card{padding:14px}h2{font-size:25px}.notes{font-size:15px}}"""

SCRIPT = """
document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>{
  document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause();});
}));
const KEY='ep009-shorts-004-rulings';
function load(){try{return JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){return {};}}
function save(s){try{localStorage.setItem(KEY,JSON.stringify(s));}catch(e){}}
const state=load();
document.querySelectorAll('[data-short]').forEach(card=>{
  const id=card.dataset.short;
  const saved=state[id]||{};
  card.querySelectorAll('input[type=radio]').forEach(r=>{
    if(saved.verdict===r.value)r.checked=true;
    r.addEventListener('change',()=>{state[id]=Object.assign(state[id]||{},{verdict:r.value});save(state);status();});
  });
  const note=card.querySelector('textarea');
  if(saved.note)note.value=saved.note;
  note.addEventListener('input',()=>{state[id]=Object.assign(state[id]||{},{note:note.value});save(state);});
});
function status(){
  const done=Object.values(state).filter(v=>v&&v.verdict).length;
  document.getElementById('status').textContent=done+' of 4 ruled on.';
}
document.getElementById('copy').addEventListener('click',()=>{
  const lines=['EP009 SHORTS-004 owner rulings',''];
  document.querySelectorAll('[data-short]').forEach(card=>{
    const id=card.dataset.short, s=state[id]||{};
    lines.push(id+' '+card.dataset.title);
    lines.push('  verdict: '+(s.verdict||'(none)'));
    if(s.note)lines.push('  note: '+s.note);
    lines.push('');
  });
  const text=lines.join('\\n');
  navigator.clipboard.writeText(text).then(
    ()=>{document.getElementById('status').textContent='Copied. Paste it back to the session.';},
    ()=>{document.getElementById('status').textContent=text;}
  );
});
status();
"""


def main() -> None:
    L.assert_locked()
    QA.mkdir(parents=True, exist_ok=True)
    (QA / "videos").mkdir(exist_ok=True)
    (QA / "posters").mkdir(exist_ok=True)

    cards = []
    candidates = []
    for slug in ORDER:
        base = P / slug
        contract = json.loads((base / "source-contract.json").read_text())
        manifest = json.loads((base / "manifest.json").read_text())["scripts"][0]
        validation = json.loads((base / "CONTRACT-VALIDATION.json").read_text())
        video = base / "review" / f"{slug}-r4.mp4"
        assert video.exists(), video
        num = manifest["id"]

        target = QA / "videos" / f"short-{num}.mp4"
        if target.is_symlink() or target.exists():
            target.unlink()
        target.symlink_to(os.path.relpath(video, target.parent))
        poster = QA / "posters" / f"short-{num}.jpg"
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                        "-ss", "0.4", "-i", str(video), "-frames:v", "1",
                        "-q:v", "3", str(poster)], check=True)

        pin = html.escape(manifest["pinned_comment"])
        cards.append(f"""<article class="card" id="short-{num}" data-short="{num}" data-title="{html.escape(manifest['title'])}">
<div class="meta">SHORT {num} <span>{contract['duration']:.2f} s &middot; {contract['frame_count']} frames</span></div>
<h2>{html.escape(manifest['title'])}</h2>
<video id="video-{num}" controls playsinline preload="metadata" poster="posters/short-{num}.jpg"><source src="videos/short-{num}.mp4" type="video/mp4"></video>
<div class="notes">
<section><b>Payoff, spoken inside the Short</b><p class="spoken">&ldquo;{html.escape(manifest['payoff_line'])}&rdquo;</p></section>
<section><b>Last thing you hear</b><p class="spoken">&ldquo;{html.escape(manifest['closing_line'])}&rdquo;</p></section>
<section><b>Cold viewer is told</b><p>{html.escape(manifest['cold_viewer_context'])}</p></section>
<section><b>Pinned comment</b><pre>{pin}</pre></section>
<section><b>What changed</b><p>{html.escape(RECUT[slug])}</p></section>
<section><b>Honest weakness</b><p>{WEAKNESS[slug]}</p></section>
<section><b>Contract validator</b><p>exit {validation['exit_code']}, valid: {str(validation['stdout']['valid']).lower()}, {len(validation['stdout']['issues'])} issues</p></section>
</div>
<div class="ruling">
<label><input type="radio" name="verdict-{num}" value="accept"> Accept</label>
<label><input type="radio" name="verdict-{num}" value="return"> Return</label>
<textarea placeholder="What to change, if you are returning it"></textarea>
</div>
</article>""")

        candidates.append({
            "id": num, "slug": slug, "title": manifest["title"],
            "duration": contract["duration"], "frame_count": contract["frame_count"],
            "width": 1080, "height": 1920,
            "payoff_line": manifest["payoff_line"],
            "closing_line": manifest["closing_line"],
            "pinned_comment": manifest["pinned_comment"],
            "video": {"path": str(video.relative_to(L.REPO)), "sha256": L.sha(video)},
            "manifest": str((base / "manifest.json").relative_to(L.REPO)),
            "contract_validation": str((base / "CONTRACT-VALIDATION.json").relative_to(L.REPO)),
            "owner_approved": False, "published": False, "related_video_bound": False,
        })

    nav = "".join(
        f'<a href="#short-{c["id"]}">{c["id"]} &middot; {html.escape(c["title"].split(",")[0])}</a>'
        for c in candidates)
    document = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow">
<title>EP009 Shorts R4 &middot; standalone payoff</title>
<style>{CSS}</style></head><body><main>
<header>
<div class="eyebrow">THE OPERATOR ECONOMY &middot; EP009 &middot; SHORTS R4 &middot; PRIVATE REVIEW</div>
<h1>Four Shorts that<br>finish their own point.</h1>
<p>Each one now orients a cold viewer in its own speech and resolves one narrow answer before it
ends. No end card asks a question the Short does not answer. The pinned comment and the related
video only add depth.</p>
<p class="tip">Play each with sound, then accept or return it. Shown in publish order: 01, 04,
02, 03. The episode link is still the literal placeholder; nothing is uploaded and the related
video is unbound.</p>
<nav>{nav}</nav>
</header>
<div class="grid">{''.join(cards)}</div>
<div class="bar"><button id="copy" type="button">Copy the four rulings</button><span id="status"></span></div>
<footer>
<p>Private review. Awaiting your creative acceptance; the full episode lock does not release
these. Built only from the locked r8 carrier, the r3 narration master and the accepted
look-transfer natives. No provider call, no generation, no retime.</p>
<p>The four superseded r3 renders are listed, with what replaces each one, in
<code>EP009-SHORTS-004/superseded/README.md</code>. Judgment per Short:
<code>EP009-SHORTS-004/STANDARD-JUDGMENT.md</code>. Mechanical checks:
<code>EP009-SHORTS-004/VERIFICATION.json</code>. Those paths are repo paths, not links from
this page; the review host only serves this directory.</p>
</footer>
</main><script>{SCRIPT}</script></body></html>"""
    (QA / "index.html").write_text(document)

    L.write_json(P / "REVIEW-PACKAGE.json", {
        "status": "private_playable_review_ready",
        "revision": "EP009-SHORTS-004",
        "supersedes": "blueprint-cinema/experiments/EP009-SHORTS-003/REVIEW-PACKAGE.json",
        "standard": "standalone payoff, docs/content-rubric.md",
        "owner_ruling": "ep009-owner-shorts-standard-ruling-v1",
        "episode_slug": "direct-booking-practice",
        "episode_url": "[EPISODE_URL]",
        "page": str((QA / "index.html").relative_to(L.REPO)),
        "page_sha256": L.sha(QA / "index.html"),
        "review_url": "https://mini.tail1c89f5.ts.net:3071/ep009-shorts-r4/",
        "publish_order": [c["id"] for c in candidates],
        "candidates": candidates,
        "longform_locked": True,
        "shorts_owner_approved": False,
        "published": False,
        "upload": False,
        "note": "The page records verdicts in the reviewer's own browser only. Nothing on it "
                "constitutes acceptance; an owner ruling is a decision-log feedback event.",
    })
    print(json.dumps({"page": str((QA / "index.html").relative_to(L.REPO)),
                      "candidates": [c["id"] for c in candidates]}, indent=2))


if __name__ == "__main__":
    main()
