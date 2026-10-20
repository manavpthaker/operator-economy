#!/usr/bin/env python3
"""Search idealab.ai and read idea briefs for the scout and research bench.

idealab.ai (Idealab.AI, Inc., Bill Gross) is a free database of ~1.2M AI-written business ideas.
Its ideas are search prompts and substitute checklists only, never buyer-side evidence; see
operator-blueprint-v2/00-intake/OWNER-DECISION-2026-10-20-IDEALAB-SOURCE.md.

Visitors (no account) get 50 searches and 10 opened briefs a day. The visitor cookie is kept in
~/.cache/oe-idealab/cookies.txt so every run shares one visitor and its honest daily allowance.

  python3 automation/tools/idealab.py search "<what the buyer needs>" [--filters JSON] [--limit N] [--out F]
  python3 automation/tools/idealab.py brief <idea id> [--out F]
  python3 automation/tools/idealab.py codes

Useful filters for the Operator Economy thesis:
  {"teamSize": ["solo", "team_2_5"], "buildType": ["HS"], "capitalBand": ["c0_10k", "c10_50k", "c50_100k"]}
  {"teamSize": ["solo", "team_2_5"], "evidenceType": ["consumer_complaint", "forum_post"]}
"""
import argparse
import http.cookiejar
import json
import os
import sys
import urllib.error
import urllib.request
import uuid

BASE = "https://idealab.ai"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
COOKIES = os.path.expanduser("~/.cache/oe-idealab/cookies.txt")

CODES = {
    "teamSize": "solo, team_2_5, team_6_20, team_21_100, workforce_heavy",
    "buildType (one)": "SW software, HS human-delivered service, OP physical ops, FN financial product, "
                       "HW hardware, LM lab science",
    "capitalBand": "c0_10k, c10_50k, c50_100k, c100_250k, c250_500k, c500k_1m, c1_2m5, ...",
    "vehicle": "studio_build (Highly Automatable), hand_to_founder, license_or_sell, non_profit_or_gov, shelve",
    "signalFamily": "opportunity, enabler, shift",
    "evidenceType": "consumer_complaint, forum_post, news_article, financial_filing, patent, "
                    "scientific_paper, standard_specification, safety_recall_warning, web_page, other_unknown",
    "geoScope": "hyperlocal, local, metro, regional, national, multinational, global",
    "numbers": "ttmMax (months), tamMin, tamMax ($bn)",
}


class Client:
    def __init__(self):
        os.makedirs(os.path.dirname(COOKIES), exist_ok=True)
        self.jar = http.cookiejar.MozillaCookieJar(COOKIES)
        if os.path.exists(COOKIES):
            self.jar.load(ignore_discard=True, ignore_expires=True)
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))
        if not any(c.name == "discover_visitor" for c in self.jar):
            self._visit()

    def call(self, path, body=None, headers=None):
        h = {"User-Agent": UA, "Origin": BASE, "Referer": BASE + "/", "Content-Type": "application/json"}
        h.update(headers or {})
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(BASE + path, data=data, headers=h, method="POST" if data else "GET")
        try:
            with self.opener.open(req, timeout=60) as r:
                status, payload = r.status, json.loads(r.read() or b"null")
        except urllib.error.HTTPError as e:
            status, payload = e.code, json.loads(e.read() or b"null")
        self.jar.save(ignore_discard=True, ignore_expires=True)
        return status, payload

    def _visit(self):
        status, _ = self.call("/api/visit", {
            "kind": "navigation", "route": "/", "pageLoadId": str(uuid.uuid4()),
            "client": {"viewportWidth": 1440, "viewportHeight": 900, "screenWidth": 1440,
                       "screenHeight": 900, "pixelRatio": 2, "touchPoints": 0, "languages": ["en-US"],
                       "timeZone": "America/New_York", "referrer": None, "platform": "macOS",
                       "mobile": False, "brands": []},
            "navigationType": "client"})
        if status != 200:
            sys.exit(f"idealab.ai visitor session failed (HTTP {status})")

    def search(self, query, filters=None, limit=25):
        body = {"query": query, "limit": min(limit, 25), "includeTotal": True}
        if filters:
            body["filters"] = filters
        return self.call("/api/idea-search", body, {"x-discover-search-source": "form"})

    def brief(self, idea_id):
        status, opened = self.call(f"/api/opened-briefs/{idea_id}", {})
        if status != 200:
            return status, opened
        return self.call(f"/api/intake/ideas/{idea_id}")


def allowance(payload):
    a = (payload or {}).get("allowance") or {}
    s, b = a.get("searches", {}), a.get("briefs", {})
    return f"searches left {s.get('remaining', '?')}/{s.get('limit', '?')}, briefs left {b.get('remaining', '?')}/{b.get('limit', '?')}"


def print_search(res):
    print(f"matches: {res.get('total')} | {allowance(res)}")
    for i in res.get("ideas", []):
        print(f"{i['id']} | {i['title']} | {i.get('vehicleLabel')} | ${i.get('startCapitalUsd'):,} to start | "
              f"{i.get('timeToMarketMonths')} mo | similarity {i.get('similarity') or 0:.2f}")
        print(f"    {i.get('thesis', '')[:300]}")


def print_brief(res):
    r, idea = res["record"], res["idea"]
    m = r["market"]
    print(f"{r['id']} {r['title']}  (written by {r.get('model')}, web check {r['webCheck']['verdict']})")
    print(f"assumes: {m['teamSizeLabel']}, ${m['startCapitalUsd']:,} to start, "
          f"${(m.get('revenueAtSuccessUsd') or 0):,} revenue at success, {m['geoScopeName']}")
    print("sources:", ", ".join(f"{s['name']} {s['n']}" for s in idea.get("sourceCounts") or []),
          "| publishers:", ", ".join(p["host"] for p in r.get("publishers", [])))
    print("scores (idealab's own, never evidence):", r.get("priors"))
    for label, key in [("pitch", "pitch"), ("buyer", "firstCustomers"), ("why now", "whyNow"),
                       ("landscape", "landscape")]:
        print(f"\n{label}: {r.get(key)}")
    print("\ncompetitors (verify each on its own page before citing):")
    for c in r.get("competitors", []):
        print(f"  - {c['name']} {c['url']}: {c['what'][:200]}")
    print("\nwhat could kill it:")
    for k in r.get("whatCouldKillIt", []):
        print(f"  - {k}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--filters", help="JSON object of filter codes")
    s.add_argument("--limit", type=int, default=25)
    s.add_argument("--out", help="also save the raw JSON here")
    b = sub.add_parser("brief")
    b.add_argument("id", type=int)
    b.add_argument("--out")
    sub.add_parser("codes")
    a = ap.parse_args()

    if a.cmd == "codes":
        for k, v in CODES.items():
            print(f"{k}: {v}")
        return
    client = Client()
    if a.cmd == "search":
        status, res = client.search(a.query, json.loads(a.filters) if a.filters else None, a.limit)
    else:
        status, res = client.brief(a.id)
    if status != 200:
        sys.exit(f"HTTP {status}: {res}")
    if a.out:
        with open(a.out, "w") as f:
            json.dump(res, f, indent=1)
    print_search(res) if a.cmd == "search" else print_brief(res)


if __name__ == "__main__":
    main()
