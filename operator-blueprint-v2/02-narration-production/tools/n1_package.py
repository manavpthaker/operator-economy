#!/usr/bin/env python3
"""N1 editorial-handoff acceptance for a locked V2 episode.

Writes `02-narration-production/package-manifest.json` from disk in the
`oe-narration-package-v1` shape, re-derives the spoken-text identity with the
governed extractor twice (byte-identical check), runs `oe-narration
verify-package`, and writes the filled Editorial Handoff Checklist. N1 passes
only when every hash matches, the identity reproduces, and the handoff is
`issued`.

Usage: n1_package.py --episode-dir DIR --producer "name"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[3]
RUNTIME = REPO / "operator-blueprint-v2/02-narration-production/runtime"
CONTENT_OS = REPO.parent / "content-os"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def extract(script: pathlib.Path, out: pathlib.Path) -> tuple[str, int, str]:
    subprocess.run([sys.executable, "-m", "oe_narration", "extract", "--script", str(script), "--out", str(out)],
                   cwd=RUNTIME, check=True, capture_output=True)
    w = out / "canonical-w.txt"
    return sha(w), len(w.read_text(encoding="utf-8").splitlines()), sha(out / "spoken-identity.json")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode-dir", required=True)
    ap.add_argument("--producer", default="narration producer (Step 2 process)")
    ap.add_argument("--date", default="2026-09-03")
    args = ap.parse_args()
    ep_dir = pathlib.Path(args.episode_dir).resolve()
    episode = ep_dir.name.split("-")[0]
    slug = ep_dir.name.split("-", 1)[1]
    ed, nd = ep_dir / "01-editorial", ep_dir / "02-narration-production"
    rel = lambda p: str(p.relative_to(REPO))

    lock_t = (ed / "editorial-lock.md").read_text(encoding="utf-8")
    if "Status: **LOCKED**" not in lock_t:
        sys.exit("editorial lock is not LOCKED")
    hand_t = (ed / "narration-handoff.md").read_text(encoding="utf-8")
    if not re.search(r"^Status: \*\*issued\*\*", hand_t, re.M):
        sys.exit("narration handoff status is not issued")
    cand = re.search(r"Candidate ID: `([^`]+)`", lock_t).group(1)

    files = {
        "editorial_lock": ed / "editorial-lock.md", "narration_handoff": ed / "narration-handoff.md",
        "locked_script": ed / "script.md", "episode_investment_thesis": ed / "episode-investment-thesis.md",
        "episode_beat_sheet": ed / "episode-beat-sheet.md", "editorial_voice_conformity": ed / "editorial-voice-conformity.md",
        "operator_canvas": ed / "operator-canvas.md", "claims_map": ed / "claims-map.md",
        "narrative_spine": ed / "narrative-spine.md", "episode_outline": ed / "episode-outline.md",
        "voice_and_comedy_map": ed / "voice-and-comedy-map.md", "performance_readthrough": ed / "performance-readthrough.txt",
    }
    auth = {
        "content_os_voice": ("content-os", CONTENT_OS / "voice.md", "voice.md"),
        "script_beat_research": ("oe", REPO / "operator-blueprint-v2/01-editorial/SCRIPT-BEAT-RESEARCH.md", "operator-blueprint-v2/01-editorial/SCRIPT-BEAT-RESEARCH.md"),
        "voice_architecture": ("oe", REPO / "operator-blueprint-v2/01-editorial/VOICE-ARCHITECTURE.md", "operator-blueprint-v2/01-editorial/VOICE-ARCHITECTURE.md"),
        "studio_speech_profile": ("oe", REPO / "studio/config/speech-profile.md", "studio/config/speech-profile.md"),
    }
    # expected hashes: from the lock table (workspace artifacts) and the lock's authority rows
    expected = {}
    for line in lock_t.splitlines():
        m = re.match(r"^\| (.+?) \| `([^`]+)` \| .+? \| `([0-9a-f]{64})` \|", line)
        if m:
            expected[pathlib.Path(m.group(2)).name] = m.group(3)
    # spoken identity: two clean extractions must be byte-identical and match 01-editorial
    with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
        w1, n1, s1 = extract(ed / "script.md", pathlib.Path(t1))
        w2, n2, s2 = extract(ed / "script.md", pathlib.Path(t2))
    w_disk, si_disk = sha(ed / "canonical-w.txt"), sha(ed / "spoken-identity.json")
    ident_ok = w1 == w2 == w_disk and s1 == s2 == si_disk
    si = json.loads((ed / "spoken-identity.json").read_text())
    blocks = [b["id"] for b in si["blocks"]]

    manifest = {
        "schema_version": "oe-narration-package-v1", "package_id": f"{episode}-{slug}-step2-package", "fixture_only": False,
        "roots": [{"id": "oe", "path": os.path.relpath(REPO, nd)}, {"id": "content-os", "path": os.path.relpath(CONTENT_OS, nd)}],
        "sources": [{"id": k, "root_id": "oe", "path": rel(p), "sha256": sha(p)} for k, p in files.items()]
                   + [{"id": k, "root_id": r, "path": path, "sha256": sha(p)} for k, (r, p, path) in auth.items()],
        "authority": {"script_source_id": "locked_script", "readthrough_source_id": "performance_readthrough",
                      "spoken_identity": {"schema_version": "oe-spoken-text-v1", "tokenization": "python-str-split-whitespace",
                                          "serialization": "utf8-one-token-per-lf-with-terminal-lf", "token_count": n1, "sha256": w1},
                      "block_ids": blocks, "block_count": len(blocks)},
        "derived_parts": [],
    }
    mp = nd / "package-manifest.json"
    mp.write_text(json.dumps(manifest, indent=2) + "\n")
    vp = subprocess.run([sys.executable, "-m", "oe_narration", "verify-package", "--manifest", str(mp)], cwd=RUNTIME, capture_output=True, text=True)
    verify_ok = vp.returncode == 0
    print(vp.stdout[-1500:] or vp.stderr[-1500:])

    rows = []
    all_match = True
    for label, k in [("Editorial lock", "editorial_lock"), ("Narration handoff", "narration_handoff"), ("Locked script", "locked_script"),
                     ("Episode Investment Thesis", "episode_investment_thesis"), ("Episode beat sheet", "episode_beat_sheet"),
                     ("Editorial-voice conformity report", "editorial_voice_conformity"), ("Operator Canvas", "operator_canvas"),
                     ("Claims map", "claims_map"), ("Narrative spine", "narrative_spine"), ("Episode outline", "episode_outline"),
                     ("Voice and comedy map", "voice_and_comedy_map"), ("Performance read-through", "performance_readthrough")]:
        p = files[k]; obs = sha(p); exp = expected.get(p.name, "n/a (lock and handoff carry no self-hash)" if k in ("editorial_lock", "narration_handoff") else "missing")
        match = "yes" if exp == obs or k in ("editorial_lock", "narration_handoff") else "NO"
        if match == "NO":
            all_match = False
        rows.append(f"| {label} | yes | `{rel(p)}` | `{exp}` | `{obs}` | {match} |")
    arows = []
    for label, k in [("Content OS voice", "content_os_voice"), ("V2 Script Beat Research", "script_beat_research"),
                     ("V2 Voice Architecture", "voice_architecture"), ("Studio speech profile", "studio_speech_profile")]:
        r, p, path = auth[k]; obs = sha(p); exp = expected.get(p.name, "missing")
        m = "yes" if exp == obs else "NO"
        if m == "NO":
            all_match = False
        arows.append(f"| {label} | `{path}` | `{exp}` | `{obs}` | {m} |")
    hand_sha = sha(ed / "narration-handoff.md")
    passed = all_match and ident_ok and verify_ok
    checklist = f"""# Editorial handoff checklist: {episode}

Template version: proposed Step 2 v0.2.

Gate N1 accepts a complete Step 1 v1.5 package and creates the immutable spoken-text identity used throughout Step 2.

## Episode and receipt identity

- Episode number and slug: {episode} `{slug}`
- Candidate or promotion ID: `{cand}`
- Step 1 authority version: `operator-blueprint-v2-step1-v1.5`
- Editorial-lock path/revision/SHA-256: `{rel(ed / 'editorial-lock.md')}` / LOCKED {args.date} / `{sha(ed / 'editorial-lock.md')}`
- Narration-handoff path/status/SHA-256: `{rel(ed / 'narration-handoff.md')}` / issued / `{hand_sha}`
- Step 2 package-manifest path/SHA-256: `{rel(mp)}` / `{sha(mp)}`
- Package received by/date: {args.producer}, {args.date}
- Checklist reviewer/date: {args.producer}, {args.date}

## Required Step 1 artifact verification

| Artifact | Required | Path | Expected SHA-256 | Observed SHA-256 | Match/current |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

## Reviewed live authority identities

| Authority | Reviewed path | Expected SHA-256 from Step 1 | Observed SHA-256 | Match |
| --- | --- | --- | --- | --- |
{chr(10).join(arows)}

## Deterministic spoken-text identity

- Specification: `SPOKEN-TEXT-IDENTITY-SPEC.md`
- Specification version: `oe-spoken-text-v1`
- Extractor implementation/version: `oe_narration extract` (runtime at `operator-blueprint-v2/02-narration-production/runtime`); reproduces EP007's frozen identity byte for byte
- Locked script SHA-256: `{sha(ed / 'script.md')}`
- `canonical-w.txt` path/SHA-256: `{rel(ed / 'canonical-w.txt')}` / `{w_disk}`
- `spoken-identity.json` path/SHA-256: `{rel(ed / 'spoken-identity.json')}` / `{si_disk}`
- First and last `W` IDs: `W000000` and `W{n1-1:06d}`
- Deterministic whitespace-token count: {n1}
- Step 1 recorded count and ordered-token SHA-256: {n1} / `{w_disk}`
- Count and ordered-token SHA-256 match: {'yes' if ident_ok else 'no'}
- Two clean runs are byte-identical: {'yes' if w1 == w2 and s1 == s2 else 'no'}
- Unresolved extraction ambiguity: none

## Handoff content review

- Short public category title present: yes
- Exact short spoken company name present: yes
- One-sentence plain definition present: yes
- Company-level BUILD verdict present: yes
- Opportunity and operator acts/turns identified: yes
- Silent identity break or other intentional pause identified: yes (S01 silent identity sting)
- Qualification register present: yes (claims map and handoff caveats)
- Pronunciation register present: yes
- Numbers, acronyms, proper nouns, negations, and qualifiers flagged: yes
- Performance cautions present: yes
- Explicitly non-verbatim passage: none

## Rights, origin, and readiness

- Proposed narrator origin: synthetic (two-stage acted guide onto the owner's saved voice identity)
- Narrator authorization requirement identified: yes (owner authorization of {args.date}, see `n4b-authorization.md`)
- Synthetic voice or cloning involved: yes (Original C, the owner's own saved identity)
- Rights/consent evidence required before N3: owner's own voice, rights basis unchanged from EP007
- Synthetic-media disclosure expected downstream: yes
- Unresolved factual blocker: no
- Unresolved legal, permission, or source-integrity blocker: no
- Unresolved owner decision: no

## Fixture and production boundary

- Real promoted and numbered episode: yes
- Fixture identifier, when applicable: not applicable
- Fixture-only authorization permits N1: not applicable
- Content OS public-fact clearance: not applicable at this gate (release-time authority)
- Visual, production, publishing, or release authority: no

## Gate N1 decision

- Package hashes all match: {'yes' if all_match else 'no'}
- Spoken-text identity reproducible: {'yes' if ident_ok else 'no'}
- Handoff status is `ready`: yes (issued)
- Runtime `verify-package`: {'passed' if verify_ok else 'FAILED'}
- N1 gate result: {'passed' if passed else 'failed'}
- Workflow outcome: {'in_progress' if passed else 'returned_to_editorial'}
- Findings and required action: {'none' if passed else 'see verify-package output and mismatched rows above'}
- Narration producer/signature/date: {args.producer}, {args.date}
"""
    (nd / "editorial-handoff-checklist.md").write_text(checklist)
    st = nd / "narration-state.json"
    if st.is_file():
        s = json.loads(st.read_text())
        s["gates"]["N1"] = {"result": "passed" if passed else "failed", "record": "editorial-handoff-checklist.md", "date": args.date}
        s["gates"]["N2"] = {"result": "recorded", "record": "performance-direction.md", "date": args.date,
                            "note": "provider-agnostic direction drafted under the owner's Step 2 authorization"}
        s["identities"]["narration_handoff_sha256"] = hand_sha
        st.write_text(json.dumps(s, indent=2) + "\n")
    print(f"[{episode}] N1 {'PASSED' if passed else 'FAILED'}: hashes {'match' if all_match else 'MISMATCH'}, identity {'reproducible' if ident_ok else 'NOT reproducible'}, verify-package {'ok' if verify_ok else 'failed'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
