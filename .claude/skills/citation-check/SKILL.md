---
name: citation-check
description: Measure whether ChatGPT, Claude and Perplexity cite Stories We Tell when buyers ask about African tech storytelling, and turn the gaps into page and post fixes. Runs every Monday; also use when asked "are we showing up in AI answers".
---

# AI citation check

## 1. Run (skip if this week's run already exists in `outputs/citations/`)
```
python scripts/citation_check.py
```
Needs any of `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `PERPLEXITY_API_KEY`. Engines without a key are skipped and noted. It writes `outputs/citations/<date>/raw.jsonl` and `summary.md`.

## 2. Analyse (write `outputs/citations/<date>/analysis.md`)
- **Share of answer**: % of questions where any engine mentions us, per engine and per vertical. Compare with last week's `summary.md`.
- **Who wins instead**: top 10 cited domains and brands. For the top 5, open one cited page each and note the traits it shares with the others:
  direct answer in the first paragraph? original numbers? named author with credentials? date? schema / FAQ? listicle position?
- **Gap list**: the 10 questions most valuable to us (vertical 6 and buyer-intent questions first) where we're absent.
- **Fix list**: for each gap, the single page or post that would best earn the citation:
  existing page to rewrite (on storieswetell.xyz) or new page/post, plus the traits to copy. Keep it to 10.
- If our site is missing `llms.txt`, Organization/Person schema, author bylines or clear service pages, put that at the top: it's cheap and lifts everything.

## 3. Hand off
Feed the fix list into next week's `/weekly-plan` as `[CITATION]` items. Log the run with `scripts/log_action.py`.

## Honesty
AI answers vary run to run. Treat a single week as noise; report trends over 4+ weeks. Never claim a citation you didn't see in `raw.jsonl`.
