---
name: weekly-plan
description: Plan next week's Stories We Tell content calendar across LinkedIn, Instagram, YouTube, X and the website, mapped to the six series. Use every Friday, or when asked "what are we posting next week".
---

# Weekly content plan

## Inputs (read all that exist)
1. `CLAUDE.md`: channels, cadence, series, voice.
2. The latest `outputs/listening/*/hooks.md`: what the market is complaining about this week.
3. The latest `outputs/citations/*/summary.md`: which questions we're invisible on.
4. The latest `outputs/reports/*.md`: what worked last week, and the suggested next test.
5. The last 4 weeks of `drafts/plan-*.md`: don't repeat angles.
6. `data/listening/inbox.md`: anything Meave flagged by hand.

## Rules
- Hit the cadence in CLAUDE.md. If the founders said capacity is low this week, cut X volume first, LinkedIn last.
- Rotate series: no series twice in a row on LinkedIn; every series at least once every two weeks.
- At least **one LinkedIn post per week is built from a listening pain point** (quote the pain in our words, answer it with evidence).
- At least **one piece per week targets a citation gap**: a question where AI assistants cite others and not us. Mark it `[CITATION]`.
- Every item carries: channel, day, series, vertical, format, working hook, the evidence/source it rests on, and **goal** (reputation / audience / pipeline).
- Include one "proof of work" item that reuses existing footage (Afribit, Orbit, Artizen Salon). Unreleased Artizen Salon footage is a priority until it's out.
- Flag anything needing Vivianna (visuals, video edit) as `[VIV]`, and anything needing Meave's personal voice or presence as `[MEAVE]`.

## Output
Write `drafts/plan-YYYY-MM-DD.md` (date = the Monday of the planned week) as a table, then a 3-line "why this week" note. Then log it:

```
python scripts/log_action.py --action "weekly plan for <date>" --reason "<one line>" --files drafts/plan-<date>.md
```
