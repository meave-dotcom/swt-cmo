#!/usr/bin/env python3
"""Ask ChatGPT, Claude and Perplexity the buyer questions in data/buyer_questions.csv
and log which brands and URLs each answer cites.

Usage:
    python scripts/citation_check.py              # all questions, every engine with a key
    python scripts/citation_check.py --limit 5    # quick test
    python scripts/citation_check.py --dry-run    # no API calls, fake answers (tests the pipeline)

Env vars (any subset; engines without a key are skipped):
    OPENAI_API_KEY      OPENAI_MODEL (default gpt-4.1)       OPENAI_SEARCH_TOOL (default web_search)
    ANTHROPIC_API_KEY   ANTHROPIC_MODEL (default claude-sonnet-5-5)
                        ANTHROPIC_SEARCH_TOOL (default web_search_20250305)
    PERPLEXITY_API_KEY  PERPLEXITY_MODEL (default sonar)
Model and tool names change; if an engine errors, check its docs and update the env var.
"""
import argparse, csv, datetime as dt, json, os, re, sys, time, urllib.request, urllib.error
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
URL_RE = re.compile(r"https?://[^\s\"'<>\)\]\\]+")


def load_yaml(path):
    import yaml  # pip install pyyaml
    return yaml.safe_load(path.read_text())


def post_json(url, headers, payload, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST",
                                 headers={"content-type": "application/json", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def ask_openai(q):
    data = post_json("https://api.openai.com/v1/responses",
                     {"authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
                     {"model": os.getenv("OPENAI_MODEL", "gpt-4.1"),
                      "tools": [{"type": os.getenv("OPENAI_SEARCH_TOOL", "web_search")}],
                      "input": q})
    text = " ".join(c.get("text", "") for o in data.get("output", []) if o.get("type") == "message"
                    for c in o.get("content", []))
    return text, data


def ask_anthropic(q):
    data = post_json("https://api.anthropic.com/v1/messages",
                     {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"},
                     {"model": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5"), "max_tokens": 1500,
                      "tools": [{"type": os.getenv("ANTHROPIC_SEARCH_TOOL", "web_search_20250305"),
                                 "name": "web_search", "max_uses": 3}],
                      "messages": [{"role": "user", "content": q}]})
    text = " ".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    return text, data


def ask_perplexity(q):
    data = post_json("https://api.perplexity.ai/chat/completions",
                     {"authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}"},
                     {"model": os.getenv("PERPLEXITY_MODEL", "sonar"),
                      "messages": [{"role": "user", "content": q}]})
    text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return text, data


ENGINES = {"chatgpt": ("OPENAI_API_KEY", ask_openai),
           "claude": ("ANTHROPIC_API_KEY", ask_anthropic),
           "perplexity": ("PERPLEXITY_API_KEY", ask_perplexity)}


def fake_answer(engine, q):
    """Deterministic fake for --dry-run."""
    if "documentary" in q.lower():
        return ("Stories We Tell (storieswetell.xyz) made the Afribit documentary.",
                {"citations": ["https://storieswetell.xyz/", "https://techcabal.com/x"]})
    return ("Try TechCabal or Techpoint Africa.",
            {"citations": ["https://techcabal.com/a", "https://techpoint.africa/b"]})


def domain(u):
    d = urlparse(u).netloc.lower()
    return d[4:] if d.startswith("www.") else d


def find_brands(text, urls, brands):
    hay = (text + " " + " ".join(urls)).lower()
    return [name for name, terms in brands.items() if any(t.lower() in hay for t in terms)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    cfg = load_yaml(ROOT / "data/brands.yaml")
    ours = cfg["ours"]["terms"]
    brands = {"Stories We Tell (us)": ours, **{p["name"]: p["terms"] for p in cfg.get("peers", [])}}
    with open(ROOT / "data/buyer_questions.csv", newline="") as f:
        qs = list(csv.DictReader(f))[: a.limit or None]

    engines = {n: fn for n, (key, fn) in ENGINES.items() if a.dry_run or os.getenv(key)}
    skipped = [n for n in ENGINES if n not in engines]
    if not engines:
        sys.exit("No API keys set. Set at least one of OPENAI_API_KEY, ANTHROPIC_API_KEY, PERPLEXITY_API_KEY, or use --dry-run.")

    today = dt.date.today().isoformat()
    out = ROOT / "outputs/citations" / today
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    with open(out / "raw.jsonl", "w") as raw:
        for q in qs:
            for name, fn in engines.items():
                try:
                    text, data = fake_answer(name, q["question"]) if a.dry_run else fn(q["question"])
                    err = None
                except (urllib.error.URLError, KeyError, ValueError) as e:
                    text, data, err = "", {}, f"{type(e).__name__}: {getattr(e, 'code', '')} {e}"
                urls = sorted(set(u.rstrip(".,;") for u in URL_RE.findall(text + json.dumps(data))))
                row = {"date": today, "id": q["id"], "vertical": q["vertical"], "intent": q["intent"],
                       "question": q["question"], "engine": name, "error": err,
                       "brands": find_brands(text, urls, brands), "urls": urls, "answer": text[:4000]}
                raw.write(json.dumps(row) + "\n")
                rows.append(row)
                if not a.dry_run:
                    time.sleep(1)

    write_summary(out, rows, skipped, today)
    print(f"Wrote {out/'raw.jsonl'} and {out/'summary.md'} ({len(rows)} answers)")


def write_summary(out, rows, skipped, today):
    us = "Stories We Tell (us)"
    ok = [r for r in rows if not r["error"]]
    by_engine, by_vert = defaultdict(list), defaultdict(list)
    for r in ok:
        by_engine[r["engine"]].append(us in r["brands"])
        by_vert[r["vertical"]].append(us in r["brands"])
    pct = lambda xs: f"{100 * sum(xs) / len(xs):.0f}% ({sum(xs)}/{len(xs)})" if xs else "n/a"
    doms = Counter(d for r in ok for d in {domain(u) for u in r["urls"]})
    brand_ct = Counter(b for r in ok for b in r["brands"])
    lines = [f"# AI citation check: {today}", "",
             f"Answers: {len(ok)} ok, {len(rows) - len(ok)} errors. Skipped engines (no key): {', '.join(skipped) or 'none'}.", "",
             "## Share of answer: how often we're mentioned", "", "| Engine | Mentioned |", "|---|---|"]
    lines += [f"| {e} | {pct(v)} |" for e, v in sorted(by_engine.items())]
    lines += ["", "| Vertical | Mentioned |", "|---|---|"]
    lines += [f"| {v} | {pct(x)} |" for v, x in sorted(by_vert.items())]
    lines += ["", "## Brands named", "", "| Brand | Answers |", "|---|---|"]
    lines += [f"| {b} | {n} |" for b, n in brand_ct.most_common(15)]
    lines += ["", "## Most-cited domains", "", "| Domain | Answers |", "|---|---|"]
    lines += [f"| {d} | {n} |" for d, n in doms.most_common(20)]
    hits = [r for r in ok if us in r["brands"]]
    lines += ["", "## Where we showed up", ""] + ([f"- [{r['engine']}] {r['question']}" for r in hits] or ["- nowhere yet"])
    errs = [r for r in rows if r["error"]]
    if errs:
        lines += ["", "## Errors", ""] + sorted({f"- {r['engine']}: {r['error'][:160]}" for r in errs})
    (out / "summary.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
