#!/usr/bin/env python3
"""Refresh data/opensource.json from GitHub's public API.

Public data only. Private repositories are not visible to the default Actions
token, so their contribution counts come from data/private_offsets.json,
which is maintained by hand.

Usage:  python3 scripts/update_stats.py            (optional env: GITHUB_TOKEN)
"""
import json, os, pathlib, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import date

USER = "priyavrat7"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "opensource.json"
OFFSETS = ROOT / "data" / "private_offsets.json"
API = "https://api.github.com"


def get(path, params=None):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "portfolio-stats-updater",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and attempt < 3:      # rate limited: wait and retry
                time.sleep(20 * (attempt + 1)); continue
            if e.code in (404, 410, 451):
                return None
            raise
    return None


def count(query):
    data = get("/search/issues", {"q": query, "per_page": 1})
    time.sleep(2.5)                                       # stay inside the search rate limit
    if data is None:
        sys.exit(f"search failed: {query}")
    return data["total_count"]


def tracked_prs():
    """PR keys such as 'aces/Loris#11257' found as data-pr attributes in the site's pages."""
    keys = set()
    for f in list(ROOT.glob("*.html")) + list((ROOT / "fr").glob("*.html")):
        keys.update(re.findall(r'data-pr="([^"]+)"', f.read_text()))
    return sorted(keys)


def main():
    offsets = json.loads(OFFSETS.read_text())
    base = f"author:{USER} is:public"
    pub = {
        "prs": count(f"{base} type:pr"),
        "merged": count(f"{base} type:pr is:merged"),
        "open": count(f"{base} type:pr is:open"),
        "issues": count(f"{base} type:issue"),
    }
    pub["closed"] = pub["prs"] - pub["merged"] - pub["open"]   # closed without merging

    totals = {k: pub[k] + offsets.get(k, 0) for k in ("prs", "merged", "open", "closed", "issues")}
    decided = totals["merged"] + totals["closed"]
    totals["merge_rate"] = round(100 * totals["merged"] / decided) if decided else 0

    statuses = {}
    for key in tracked_prs():
        repo, num = key.rsplit("#", 1)
        pr = get(f"/repos/{repo}/pulls/{num}")
        time.sleep(0.3)
        if pr is None:
            continue                                      # private or missing: keep the page's static badge
        statuses[key] = "merged" if pr.get("merged_at") else ("open" if pr["state"] == "open" else "closed")

    result = {
        "user": USER,
        "totals": totals,
        "public_only": pub,
        "private_offsets_as_of": offsets.get("as_of"),
        "prs": statuses,
    }
    previous = json.loads(OUT.read_text()) if OUT.exists() else {}
    previous.pop("updated", None)
    if previous == result:
        print("No change.")
        return
    result["updated"] = date.today().isoformat()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("Updated", OUT.relative_to(ROOT), totals)


if __name__ == "__main__":
    main()
