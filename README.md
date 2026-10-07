# swt-cmo: the Stories We Tell CMO agent

An AI marketing lead for Stories We Tell, built on Claude Code + GitHub. It plans, researches, drafts and reports. **Humans publish.** It never posts, spends money or emails anyone but info@storieswetell.xyz.

## What it does, and when

| When (Nairobi time) | What | You get |
|---|---|---|
| **Mon 06:15** | Asks ChatGPT, Claude and Perplexity 40 buyer questions; logs who gets cited. Pulls Reddit/HN posts on comms pain points; clusters them into pains and hooks. Writes the weekly report. | Email: *SWT Monday report* |
| **Fri 09:10** | Plans next week across LinkedIn, IG, YouTube, X. Drafts the LinkedIn + X posts in your voice. | Email: *SWT plan + drafts*; drafts in `drafts/` |
| Any time | Open the repo in Claude Code and type `/weekly-plan`, `/draft-posts`, `/citation-check`, `/market-listening`, `/monday-report` | |

Everything it does is logged with a reason in `logs/actions.jsonl`.

## Switch it on (about 15 minutes)

1. **Create the repo.** On github.com (account `meave-dotcom`) → New repository → name `swt-cmo` → **Private** → create, empty.
2. **Push this folder.** Unzip, then in a terminal inside the folder:
   ```
   git remote add origin https://github.com/meave-dotcom/swt-cmo.git
   git push -u origin main
   ```
   Or drag the files into GitHub's "upload files" page.
3. **Add secrets.** Repo → Settings → Secrets and variables → Actions → New repository secret:
   - `ANTHROPIC_API_KEY` (**required**, runs the agent; console.anthropic.com)
   - `SMTP_USER` = `info@storieswetell.xyz`, `SMTP_PASS` = that mailbox's password (Hostinger email)
   - `OPENAI_API_KEY`, `PERPLEXITY_API_KEY` (optional; each adds one engine to the citation check. Without them, only Claude is checked.)
4. **Test it.** Repo → Actions → *Monday — citations, listening, report* → **Run workflow**. In ~10 minutes a report should land at info@.
5. **Every Monday morning, before 06:15**, add last week's numbers as one row in `data/metrics.csv` (edit it on GitHub). Five minutes. Without it the report covers citations and listening only.

## Running costs (rough, check current pricing)
API usage only: 40 questions × up to 3 engines weekly, plus two agent runs. Expect a few US dollars a month. GitHub Actions minutes are free at this volume on a private repo.

## What you tune
- `CLAUDE.md`: the brain. Update services, proof of work and voice as the studio evolves.
- `data/buyer_questions.csv`: add real questions prospects ask you. Grow to 100.
- `data/brands.yaml`: add the agencies/studios you actually compete with.
- `data/listening_sources.yaml`: search terms and subreddits.
- `data/listening/inbox.md`: paste LinkedIn/X posts worth learning from.

## How the 11-step playbook maps here

| Playbook step | Status | Notes |
|---|---|---|
| 1. Agent that runs the account | **Built, reshaped** | content-ops agent, not an ads bidder |
| 5. Getting cited by AI | **Built** | `citation_check.py` + `/citation-check` |
| 6. Research from reviews | **Built, reshaped** | market listening from public posts |
| 11. Automated reporting | **Built** | `/monday-report`, emailed |
| 2. Programmatic SEO | Next | page per published story / Put Us On feature, never thin pages |
| 7. Matched landing pages | Next | one page per service offer, matched to the campaign |
| 3, 4, 8, 9, 10 | Parked | need paid ads, a product or a store; revisit if that changes |

## Known limits (v1)
- LinkedIn, Instagram and X numbers are entered by hand; their APIs need business approval. A later version can connect them.
- Reddit sometimes blocks cloud servers; errors are written to `outputs/listening/<date>/errors.txt` and the run carries on.
- AI answers vary run to run. Read citation results as 4-week trends.
- Model names in `scripts/citation_check.py` are configurable by env var; if an engine errors, update its model name.
