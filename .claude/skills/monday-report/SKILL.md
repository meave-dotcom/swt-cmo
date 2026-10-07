---
name: monday-report
description: Write the Stories We Tell Monday marketing report (last week vs the week before, what changed, the next test) and email it to info@storieswetell.xyz. Runs Monday morning; also use when asked for "the weekly report".
---

# Monday report

## Inputs
1. `data/metrics.csv`: the last two rows (week_start = last week and the week before). If last week's row is missing, say so at the top of the report and still report everything else.
2. This week's `outputs/citations/<date>/summary.md` (+ `analysis.md` if present).
3. This week's `outputs/listening/<date>/clusters.md` and `hooks.md` if present.
4. `logs/actions.jsonl`: entries from the last 7 days.
5. Last week's `drafts/plan-*.md`: what was planned vs what shipped (`posts_published` in metrics).

## Write `outputs/reports/YYYY-MM-DD.md` (≤ 450 words)

```
# Stories We Tell: week of <date>

## Headline
One sentence: the single most important thing that changed.

## Numbers  (last week | week before | change)
Reputation: AI share-of-answer, press/podcast mentions
Audience: followers + engagement per channel, site visits, Put Us On submissions, contributor pitches
Pipeline: inbound enquiries, discovery calls, proposals sent, won

## What changed and why
3 bullets max. Causes, not just movement. If you don't know why, say so.

## Plan vs shipped
Planned N, shipped M. What slipped and the likely reason.

## What the market said
Top 2 listening pains, with one phrase each.

## Next test
One experiment for this week: hypothesis, what we'll do, metric, how we'll judge it.
```

Compute changes with arithmetic you actually run (python), not by eye. Don't round a small sample into a trend: with fewer than ~3 weeks of data, call movements "early signal".

## Send
```
python scripts/send_email.py --subject "SWT Monday report: <date>" --file outputs/reports/<date>.md
```
Then log with `scripts/log_action.py`. If sending fails, the report still lives in the repo; say so in the log.
