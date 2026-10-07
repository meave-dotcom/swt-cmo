#!/usr/bin/env python3
"""Pull public posts about the pains Stories We Tell solves, from Reddit and Hacker News.

Usage:
    python scripts/listening_pull.py            # every term in data/listening_sources.yaml
    python scripts/listening_pull.py --limit 3  # first 3 terms only

LinkedIn and X can't be pulled without paid APIs: paste posts into data/listening/inbox.md.
Output: outputs/listening/<date>/posts.jsonl (deduplicated against previous weeks).
"""
import argparse, datetime as dt, json, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = {"user-agent": "swt-cmo-listening/1.0 (contact: info@storieswetell.xyz)"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.loads(r.read())


def reddit(term, subs):
    out = []
    targets = [f"r/{s}/search.json?restrict_sr=1&" for s in subs] or ["search.json?"]
    for t in targets:
        url = f"https://www.reddit.com/{t}q={urllib.parse.quote(term)}&sort=new&t=year&limit=25"
        for c in get(url).get("data", {}).get("children", []):
            d = c["data"]
            out.append({"source": "reddit", "id": "rd_" + d["id"], "url": "https://www.reddit.com" + d["permalink"],
                        "title": d.get("title", ""), "text": (d.get("selftext") or "")[:3000],
                        "where": d.get("subreddit_name_prefixed", ""),
                        "created": dt.datetime.fromtimestamp(d["created_utc"], dt.timezone.utc).isoformat()})
        time.sleep(2)
    return out


def hn(term):
    since = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=365)).timestamp())
    url = ("https://hn.algolia.com/api/v1/search_by_date?tags=(story,comment)&hitsPerPage=30"
           f"&numericFilters=created_at_i>{since}&query={urllib.parse.quote(term)}")
    return [{"source": "hn", "id": "hn_" + h["objectID"],
             "url": f"https://news.ycombinator.com/item?id={h['objectID']}",
             "title": h.get("title") or h.get("story_title") or "",
             "text": (h.get("comment_text") or h.get("story_text") or "")[:3000],
             "where": "hacker news", "created": h.get("created_at", "")} for h in get(url).get("hits", [])]


def main():
    import yaml
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    cfg = yaml.safe_load((ROOT / "data/listening_sources.yaml").read_text())
    terms = cfg["terms"][: a.limit or None]

    seen = set()
    for f in (ROOT / "outputs/listening").glob("*/posts.jsonl"):
        seen |= {json.loads(l)["id"] for l in f.read_text().splitlines() if l.strip()}

    out = ROOT / "outputs/listening" / dt.date.today().isoformat()
    out.mkdir(parents=True, exist_ok=True)
    new, errors = [], []
    for term in terms:
        for name, fn in (("reddit", lambda t: reddit(t, cfg.get("subreddits", []))), ("hn", hn)):
            try:
                for p in fn(term):
                    if p["id"] not in seen:
                        seen.add(p["id"]); p["term"] = term; new.append(p)
            except Exception as e:  # network blocks are common; keep going
                errors.append(f"{name} / {term}: {type(e).__name__} {e}")
    with open(out / "posts.jsonl", "w") as f:
        for p in new:
            f.write(json.dumps(p) + "\n")
    print(f"{len(new)} new posts -> {out/'posts.jsonl'}")
    if errors:
        (out / "errors.txt").write_text("\n".join(errors) + "\n")
        print(f"{len(errors)} source errors, see {out/'errors.txt'}")


if __name__ == "__main__":
    main()
