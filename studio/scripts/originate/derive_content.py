"""
Originate Step 5: Derive LinkedIn/Grapevines content + the blueprint doc.

One research run feeds five surfaces. From the approved script this
generates:
  - blueprint.md        — the downloadable lead magnet (email capture asset)
  - newsletter.md       — Monday newsletter draft (Grapevines voice)
  - linkedin_posts.md   — N standalone posts mapped to content themes
  - shorts_briefs.json  — moments for the EXISTING viddy pipeline to cut
                          once the long-form is rendered

Usage:
    python scripts/originate/derive_content.py originate/<slug>/script.json

Output:
    originate/<slug>/content/
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

import anthropic

ROOT = Path(__file__).parent.parent.parent
REPO_ROOT = ROOT.parent
EPISODES_JSON = REPO_ROOT / "site" / "data" / "episodes.json"


def _extract_stack_cost(text: str) -> str | None:
    """Pull a '<$100/mo'-shaped clause out of an economics blurb."""
    if not text:
        return None
    m = re.search(r"(?:cost[s]?\s+)?(<\s*\$[\d,]+(?:[–\-][\d,]+)?/\w+)", text, re.IGNORECASE)
    if m:
        return m.group(1).replace(" ", "")
    return None


def _extract_honest_math(text: str) -> tuple[str | None, bool]:
    """Pull the year-one revenue range and whether it's flagged as an estimate."""
    if not text:
        return None, False
    m = re.search(
        r"(\$[\d,]+[–\-]\d+K?/\w+)\s*(?:\(estimate\)|\bestimate\b)?[^.]*?(year[- ]one|yr\s*1|yr\s*one)",
        text,
        re.IGNORECASE,
    )
    if not m:
        m = re.search(r"(\$[\d,]+[–\-]\d+K?/\w+)", text)
    if not m:
        return None, False
    raw = m.group(1)
    # Only append the "yr 1" annotation if the source didn't already say it.
    value = raw if re.search(r"yr\s*1|year\s*one", raw, re.IGNORECASE) else f"{raw} yr 1"
    is_estimate = "estimate" in text.lower() or "est." in text.lower()
    return value, is_estimate


_STAGE_ORDER = {"research": 0, "scripting": 1, "production": 2}


def _advance_stage(current: str | None, proposed: str) -> str:
    """Stages are monotonic — never move an episode backwards."""
    if not current:
        return proposed
    if proposed not in _STAGE_ORDER:
        return current
    return proposed if _STAGE_ORDER[proposed] > _STAGE_ORDER.get(current, -1) else current


def _extract_playbook_span(plan: str) -> str | None:
    """Extract a 'weeks 1-4' span from the first-customer plan, if stated."""
    if not plan:
        return None
    m = re.search(r"weeks?\s+(\d+[–\-]\d+)", plan, re.IGNORECASE)
    if m:
        return f"weeks {m.group(1)}"
    return None


def update_episodes_json(script: dict, config: dict) -> None:
    """Upsert this episode's entry in site/data/episodes.json.

    Only writes fields we can derive from script.json or config; missing
    optional fields are omitted so the site component's `!== undefined`
    checks skip them. Status defaults to `in_research` for new entries;
    an existing entry's status/date/rev are preserved (use publish.py
    to flip to `live`).
    """
    if not EPISODES_JSON.exists():
        print(f"⚠ {EPISODES_JSON.relative_to(REPO_ROOT)} not found — skipping.")
        return

    with open(EPISODES_JSON) as f:
        data = json.load(f)

    slug = script.get("slug")
    if not slug:
        print("⚠ script.json has no slug — skipping episodes.json update.")
        return

    bs = script.get("blueprint_summary") or {}
    sources = script.get("sources") or []

    entry = {
        "slug": slug,
        "title": bs.get("idea", "").split(":")[0].strip() or script.get("working_title", slug),
        "category": config.get("category", "Services"),
    }

    # Thesis: prefer an explicit thesis field; else the first sentence of the idea +
    # who_its_for. This is prose, not figures — safe to derive.
    thesis_source = script.get("thesis") or bs.get("idea")
    if thesis_source:
        entry["thesis"] = thesis_source.strip()

    if sources:
        entry["sources_verified"] = len(sources)

    stack_cost = _extract_stack_cost(bs.get("realistic_economics", ""))
    if stack_cost:
        entry["stack_cost"] = stack_cost

    math, is_est = _extract_honest_math(bs.get("realistic_economics", ""))
    if math:
        entry["honest_math"] = math
        if is_est:
            entry["honest_math_estimate"] = True

    span = _extract_playbook_span(bs.get("first_customer_plan", ""))
    if span:
        entry["playbook_span"] = span

    # Stage advances with the pipeline: derive_content runs post-script (Gate 1
    # passed), so the natural stage at this point is `production`. `new` sets
    # `research`; publish.py flips to `live`. See originate.py for the flow.
    stage = config.get("stage", "production")

    episodes = data.setdefault("episodes", [])
    existing = next((e for e in episodes if e.get("slug") == slug), None)
    if existing is None:
        entry["number"] = max((e.get("number", 0) for e in episodes), default=0) + 1
        entry["status"] = "upcoming"
        entry["stage"] = stage
        episodes.append(entry)
        action = f"appended as №{entry['number']:03d} (stage={stage})"
    else:
        # Fill-if-missing on updates: never overwrite an operator-authored title,
        # href, or a manually-cleaned figure. Fresh derivations show up as new fields.
        for k, v in entry.items():
            existing.setdefault(k, v)
        # Stage IS allowed to advance forward — this is derive stepping the pipeline.
        if existing.get("status") == "upcoming":
            existing["stage"] = _advance_stage(existing.get("stage"), stage)
        action = f"updated (№{existing.get('number', '??'):03d}, status={existing.get('status')}, stage={existing.get('stage', '—')})"

    data["updated"] = date.today().isoformat()

    with open(EPISODES_JSON, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"✓ episodes.json: {slug} {action}")

# ---------------------------------------------------------------------------
# YouTube upload metadata (deterministic — no API call)
# ---------------------------------------------------------------------------

# Human-readable chapter labels for the fixed section structure.
_CHAPTER_LABELS = {
    "hook": "The setup",
    "thesis": "The thesis",
    "evidence": "The evidence",
    "stack": "The stack",
    "playbook": "The playbook",
    "economics": "The honest math",
    "cta": "Get the blueprint",
}


def _fmt_ts(seconds: float) -> str:
    s = int(round(seconds))
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"


def _build_chapters(render_data_path: Path) -> list[str] | None:
    """Chapter lines from render_data/blueprint.json, or None pre-render.

    Section `start` values are VO-relative; the brand/title bookends play
    before them, so real video time = start + bookend offset. YouTube
    requires the first chapter at 0:00 — the hook is clamped there.
    """
    if not render_data_path.exists():
        return None
    with open(render_data_path) as f:
        rd = json.load(f)
    bookends = rd.get("bookends") or {}
    offset = (bookends.get("brand_seconds") or 0) + (bookends.get("title_seconds") or 0)
    lines = []
    for i, sec in enumerate(rd.get("sections") or []):
        label = _CHAPTER_LABELS.get(sec.get("id"), (sec.get("id") or "chapter").title())
        start = 0.0 if i == 0 else (sec.get("start") or 0) + offset
        lines.append(f"{_fmt_ts(start)} {label}")
    return lines or None


def write_youtube_metadata(script: dict, content_dir: Path) -> None:
    """Assemble youtube_metadata.md: title, description (with chapters),
    tags, pinned comment, and the upload-settings checklist.

    Channel-level boilerplate (subscribe link, channel blurb) lives in
    Studio upload defaults — do NOT duplicate it here.
    """
    slug = script.get("slug", "")
    title = script.get("working_title", slug)
    title_options = script.get("title_options") or []
    desc = (script.get("description_draft") or "").strip()
    blueprint_url = f"https://theoperatoreconomy.com/#capture"

    chapters = _build_chapters(content_dir.parent / "render_data" / "blueprint.json")
    chapters_block = (
        "\n".join(chapters)
        if chapters
        else "0:00 The setup\n(run `originate.py render` first — timestamps come from render_data/blueprint.json)"
    )

    # Topical tags: channel-wide defaults are set in Studio upload defaults;
    # these are the episode-specific ones to add on top.
    topic = (script.get("topic") or "").strip()
    idea = ((script.get("blueprint_summary") or {}).get("idea") or "").split(":")[0].strip()
    # Keep only phrase-shaped candidates — a thesis sentence is not a tag.
    tags = [t for t in {topic, idea, slug.replace("-", " ")} if t and len(t) <= 40 and len(t.split()) <= 5]

    md = f"""# YouTube upload metadata: {title}

## Title (pick one)

- {title}
{chr(10).join(f"- {t}" for t in title_options if t != title)}

## Description

{desc}

Get the full blueprint (free): {blueprint_url}

Chapters:
{chapters_block}

*(Channel boilerplate — site link, subscribe link — is appended automatically
by Studio upload defaults. Don't paste it again.)*

## Tags (episode-specific, on top of channel defaults)

{", ".join(tags) if tags else "(add 3-5 topical tags)"}

## Pinned comment

The full blueprint from this breakdown — tool stack, week-by-week playbook,
and the honest math — is free here: {blueprint_url}

## Upload checklist (settings that are NOT defaults)

- [ ] Schedule, don't publish: set live ≥24h out (processing/checks finish; Gate 3 review window)
- [ ] Altered content / AI disclosure: YES (synthetic VO) — required
- [ ] Audience: NOT made for kids
- [ ] Custom thumbnail (concepts in script.json → thumbnail_text_options)
- [ ] Upload SRT captions from VO text (don't rely on auto-captions)
- [ ] End screen: subscribe + next episode
- [ ] Add to the episodes playlist
- [ ] Post the pinned comment right after it goes live
"""
    (content_dir / "youtube_metadata.md").write_text(md)
    print(f"✓ youtube_metadata.md → {content_dir}")


SYSTEM_PROMPT = """You are the content lead for Grapevines (AI career strategy) deriving multi-surface content from a finished YouTube script. The author is Manav Thaker: founder, ex-Head of Product, operator voice — practical, specific, no hype, no emojis, no engagement-bait.

Rules:
- Every piece must stand alone (no "as I said in my video" framing; the video is linked, not required).
- LinkedIn posts (TEXT-ONLY strategy, decided 2026-07-05): 120-220 words, one idea each, line breaks for scannability, no hashtag spam (max 2), NO media. The post body NEVER contains a link — each post gets a separate `comment` field: one short comment carrying ONE link (the episode's blueprint page) with a single unsalesy line. Posts run on the OE company page. Each post maps to one theme from the provided list.
- Personal reposts: also produce `repost_blurbs` — 2 casual one-liners in Manav's voice for resharing the company post from his personal profile. "Found this useful" energy; zero self-promotion; never mentions that he made it beyond natural attribution. Staggered days, so vary the angle.
- Newsletter: 400-700 words, has a named takeaway section and links the video + blueprint.
- Blueprint doc: the actual deliverable promised in the video — idea, evidence table, tool stack with costs, week-by-week playbook, honest economics, sources. Someone should be able to act on it without watching.
- Shorts briefs: YOUTUBE-ONLY (no LinkedIn clips). INFORMATION-GAP strategy, strictly. Each Short presents the setup and first insight, then ENDS ON A CLIFFHANGER — it must never resolve the core question (complete-answer Shorts kill long-form conversion). Hook in the first line, 30-75s of VO, and a pinned_comment pointing to the full breakdown.
- Never promise income. Sourced numbers only."""


def main():
    parser = argparse.ArgumentParser(description="Derive LI/newsletter/blueprint content")
    parser.add_argument("script", help="Path to approved script.json")
    parser.add_argument("--config", default=str(ROOT / "config" / "blueprint.json"))
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)
    d_cfg = config["derivation"]
    script_path = Path(args.script)
    with open(script_path) as f:
        script = json.load(f)

    content_dir = script_path.parent / "content"
    content_dir.mkdir(exist_ok=True)

    user_prompt = f"""Themes for LinkedIn posts: {d_cfg['linkedin_themes']}
Number of LinkedIn posts: {d_cfg['linkedin_posts']}
Number of shorts briefs: {d_cfg['shorts_briefs']}
CTA assets: blueprint download (lead magnet), grapevines.ai/intel (secondary).

Script JSON:
{json.dumps(script, indent=2)}

Return JSON:
{{
  "blueprint_md": str,      // full markdown doc
  "newsletter_md": str,     // full markdown draft
  "linkedin_posts": [{{"theme": str, "post": str, "comment": str}}],
  "repost_blurbs": [str, str],
  "shorts_briefs": [{{"title": str, "section": str, "first_beat": int, "last_beat": int, "hook_line": str, "cliffhanger_line": str, "pinned_comment": str, "why": str}}]
}}"""

    client = anthropic.Anthropic()
    print("Deriving content...")
    response = client.messages.create(
        model=config["models"]["derive"],
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = re.sub(r"^```(json)?|```$", "", next(b.text for b in response.content if getattr(b, "type", "") == "text").strip(), flags=re.MULTILINE).strip()
    out = json.loads(text)

    (content_dir / "blueprint.md").write_text(out["blueprint_md"])
    (content_dir / "newsletter.md").write_text(out["newsletter_md"])

    posts_md = "\n\n---\n\n".join(
        f"**Theme: {p['theme']}**\n\n{p['post']}\n\n**→ Comment (the only link):**\n\n{p.get('comment', '')}"
        for p in out["linkedin_posts"])
    reposts = out.get("repost_blurbs", [])
    reposts_md = "\n\n".join(f"- {r}" for r in reposts)
    (content_dir / "linkedin_posts.md").write_text(
        f"# LinkedIn kit: {script['working_title']}\n\n"
        f"*(Text-only posts on the OE page; link lives in the first comment; "
        f"clips are YouTube-only. Personal profile: casual staggered reposts below.)*\n\n"
        f"{posts_md}\n\n---\n\n## Personal repost blurbs\n\n{reposts_md}\n")

    with open(content_dir / "shorts_briefs.json", "w") as f:
        json.dump(out["shorts_briefs"], f, indent=2)

    print(f"\n✓ blueprint.md, newsletter.md, {len(out['linkedin_posts'])} LI posts, "
          f"{len(out['shorts_briefs'])} shorts briefs → {content_dir}")

    write_youtube_metadata(script, content_dir)

    update_episodes_json(script, config)

    print("\nShorts: after rendering the long-form, run the standard viddy pipeline on it —")
    print("  python pipeline.py output/<slug>/blueprint_final.mp4")
    print("shorts_briefs.json tells the clip selector where to look (pass via --context).")


if __name__ == "__main__":
    main()
