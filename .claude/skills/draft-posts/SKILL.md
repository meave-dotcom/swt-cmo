---
name: draft-posts
description: Write post drafts for Stories We Tell from the current weekly plan (or a single brief), in Meave's voice, ready for human approval. Use after /weekly-plan or when asked to draft a post.
---

# Draft posts

## Inputs
- The newest `drafts/plan-*.md` (or the brief you were given).
- `CLAUDE.md` voice and channel rules.
- Sources named in the plan. Open them; don't write from memory.

## For each item, write `drafts/posts/YYYY-MM-DD-<channel>-<slug>.md` containing
1. **Primary draft**, formatted for the channel:
   - LinkedIn: 120–250 words, strong first line (≤ 12 words) that works before "…see more", short paragraphs, no link in body, link noted for first comment, 0–3 hashtags at the end.
   - X: single post ≤ 270 chars, or a thread of 4–8 posts with the claim in post 1.
   - Instagram: caption ≤ 150 words + a shot list / slide-by-slide brief for Vivianna in brand colours.
   - YouTube Short: 30–45s script with a 2-second hook, on-screen text lines, b-roll notes.
2. **Two alternate hooks** (first lines), different angles, not rewordings.
3. **Sources**: every fact, with link.
4. **Self-check**: tick each:
   - [ ] no invented quotes, people, numbers or clients
   - [ ] no banned hype words (see CLAUDE.md)
   - [ ] names and stories of real people treated accurately
   - [ ] the post makes an argument, not just an announcement
   - [ ] goal (reputation / audience / pipeline) stated

Never post. Then log one line per batch with `scripts/log_action.py`.
