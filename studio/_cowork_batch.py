"""Cowork batch runner for OE long Anthropic calls (plan_assets, derive_content)
via the Batches API so they survive the sandbox's 45s shell cap. Replicates each
script's exact prompt and writes outputs where the originals would.

Usage: python _cowork_batch.py <submit|poll> <slug> <assets|derive>
"""
import os, sys, json, re
from pathlib import Path

STUDIO = Path(__file__).parent
for line in (STUDIO / ".env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v.strip().strip('"').strip("'"))

sys.path.insert(0, str(STUDIO))
import anthropic
from scripts.originate.plan_assets import SYSTEM_PROMPT as PA_SYS, build_review_md as pa_review
from scripts.originate.derive_content import (
    SYSTEM_PROMPT as DV_SYS, write_youtube_metadata, update_episodes_json,
)

CONFIG = json.loads((STUDIO / "config" / "blueprint.json").read_text())


def sdir(slug):
    return STUDIO / "originate" / slug


def _batchfile(slug, job):
    return sdir(slug) / f".{job}_batch_id"


def _create(model, max_tokens, system, user, cid):
    c = anthropic.Anthropic()
    return c.messages.batches.create(requests=[{
        "custom_id": cid,
        "params": {"model": model, "max_tokens": max_tokens, "system": system,
                   "messages": [{"role": "user", "content": user}],
                   "thinking": {"type": "disabled"}},
    }])


def _result_text(slug, job):
    c = anthropic.Anthropic()
    bid = _batchfile(slug, job).read_text().strip()
    b = c.messages.batches.retrieve(bid)
    print("STATUS", job, b.processing_status, dict(b.request_counts))
    if b.processing_status != "ended":
        return None
    for r in c.messages.batches.results(bid):
        if r.result.type != "succeeded":
            print("FAIL", r.result.type, getattr(r.result, "error", ""))
            return None
        t = r.result.message.content[0].text.strip()
        return re.sub(r"^```(json)?|```$", "", t, flags=re.MULTILINE).strip()
    return None


# ---- assets ----
def submit_assets(slug):
    script = json.loads((sdir(slug) / "script.json").read_text())
    payload = [{"section": s["id"],
                "beats": [{"beat": b["beat"], "vo_text": b["vo_text"],
                           "asset_hint": b.get("asset_hint", ""), "source": b.get("source")}
                          for b in s.get("beats", [])]}
               for s in script["sections"]]
    user = ("Expand every beat into one asset spec. Return JSON: "
            '{"sections":[{"id":str,"assets":[{"beat":int,"spec":{...}}]}]}\n\n'
            + json.dumps(payload, indent=2))
    b = _create(CONFIG["models"]["assets"], 8000, PA_SYS, user, "assets")
    _batchfile(slug, "assets").write_text(b.id)
    print("SUBMITTED assets", b.id, b.processing_status)


def poll_assets(slug):
    text = _result_text(slug, "assets")
    if text is None:
        return
    assets = json.loads(text)
    (sdir(slug) / "assets.json").write_text(json.dumps(assets, indent=2))
    (sdir(slug) / "assets_review.md").write_text(pa_review(assets))
    n = sum(len(s["assets"]) for s in assets["sections"])
    print("WROTE assets.json —", n, "assets")


# ---- derive ----
def submit_derive(slug):
    script = json.loads((sdir(slug) / "script.json").read_text())
    d_cfg = CONFIG["derivation"]
    t_cfg = d_cfg.get("trailer") or {}
    trailer_enabled = bool(t_cfg.get("enabled"))
    trailer_lines, trailer_schema = "", ""
    if trailer_enabled:
        trailer_lines = (
            f"Trailer: yes — target ~{t_cfg.get('target_seconds', 25)}s total, "
            f"{t_cfg.get('segments', [2, 4])[0]}-{t_cfg.get('segments', [2, 4])[-1]} segments, "
            "ships Sunday evening before the Monday 11:00 ET episode.\n")
        trailer_schema = ""","\n  \"trailer_brief\": {\n    \"title\": str,\n    \"segments\": [{\"section\": str, \"first_line\": str, \"last_line\": str, \"why\": str}],\n    \"end_card_title\": str,\n    \"end_card_sub\": str,\n    \"youtube_description\": str,\n    \"linkedin_post\": str,\n    \"linkedin_comment\": str\n  }"""
    user_prompt = f"""Themes for LinkedIn posts: {d_cfg['linkedin_themes']}
Number of LinkedIn posts: {d_cfg['linkedin_posts']}
Number of shorts briefs: {d_cfg['shorts_briefs']}
{trailer_lines}CTA assets: blueprint download (lead magnet), grapevines.ai/intel (secondary).

Script JSON:
{json.dumps(script, indent=2)}

Return JSON:
{{
  "blueprint_md": str,
  "newsletter_md": str,
  "linkedin_posts": [{{"theme": str, "post": str, "comment": str}}],
  "repost_blurbs": [str, str],
  "shorts_briefs": [{{"title": str, "section": str, "first_beat": int, "last_beat": int, "hook_line": str, "cliffhanger_line": str, "pinned_comment": str, "why": str}}]{trailer_schema}
}}

Trailer segment rules (if trailer requested): `first_line`/`last_line` are EXACT
phrases from the section's vo_text (they anchor the audio cut — copy them verbatim,
4+ words each). Segments must come from >=2 different sections and stitch coherently
without connective tissue."""
    b = _create(CONFIG["models"]["derive"], 16000, DV_SYS, user_prompt, "derive")
    _batchfile(slug, "derive").write_text(b.id)
    print("SUBMITTED derive", b.id, b.processing_status)


def poll_derive(slug):
    text = _result_text(slug, "derive")
    if text is None:
        return
    out = json.loads(text)
    script = json.loads((sdir(slug) / "script.json").read_text())
    content_dir = sdir(slug) / "content"
    content_dir.mkdir(exist_ok=True)
    (content_dir / "blueprint.md").write_text(out["blueprint_md"])
    (content_dir / "newsletter.md").write_text(out["newsletter_md"])
    posts_md = "\n\n---\n\n".join(
        f"**Theme: {p['theme']}**\n\n{p['post']}\n\n**→ Comment (the only link):**\n\n{p.get('comment', '')}"
        for p in out["linkedin_posts"])
    reposts_md = "\n\n".join(f"- {r}" for r in out.get("repost_blurbs", []))
    (content_dir / "linkedin_posts.md").write_text(
        f"# LinkedIn kit: {script['working_title']}\n\n"
        f"*(Text-only posts on the OE page; link lives in the first comment; "
        f"clips are YouTube-only. Personal profile: casual staggered reposts below.)*\n\n"
        f"{posts_md}\n\n---\n\n## Personal repost blurbs\n\n{reposts_md}\n")
    (content_dir / "shorts_briefs.json").write_text(json.dumps(out["shorts_briefs"], indent=2))
    if out.get("trailer_brief"):
        tb = out["trailer_brief"]
        (content_dir / "trailer_brief.json").write_text(json.dumps(tb, indent=2))
        (content_dir / "trailer_linkedin.md").write_text(
            f"# Trailer post (OE page, Sunday evening — pre-launch)\n\n{tb['linkedin_post']}\n\n"
            f"**→ Comment (the only link):**\n\n{tb.get('linkedin_comment', '')}\n")
    write_youtube_metadata(script, content_dir)
    update_episodes_json(script, CONFIG)
    print(f"WROTE content/ — {len(out['linkedin_posts'])} LI posts, "
          f"{len(out['shorts_briefs'])} shorts briefs")


if __name__ == "__main__":
    mode, slug, job = sys.argv[1], sys.argv[2], sys.argv[3]
    {"submit": {"assets": submit_assets, "derive": submit_derive},
     "poll": {"assets": poll_assets, "derive": poll_derive}}[mode][job](slug)
