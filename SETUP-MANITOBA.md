# ManitobaBotNews: setup

This branch is a Manitoba-only, English version of the autoposter. Code (`bot.py`) is unchanged; what differs:
`config.py` (channel, time zone, feeds, history), `prompts.py` (English style guide), `state.json` (empty),
`save_state.sh` (saves to the branch it runs on), and the workflows (own environment and concurrency groups).

## One-time setup

1. **Telegram:** create the bot with @BotFather, create the channel (`@ManitobaBotNews`, or change `CHANNEL` in `config.py`),
   add the bot as a channel admin with permission to post. Start a chat with the bot yourself.
2. **GitHub environment:** repo Settings → Environments → New environment → `manitoba`. Add these environment secrets
   (they override the repo-level secrets used by the Ukrainian bot on `main`):
   `ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ADMIN_ID`; optional: `TELEGRAPH_TOKEN`, `FACEBOOK_PAGE_ID`, `FACEBOOK_PAGE_TOKEN`.
   (Needs repo admin. Without it, ask the owner to add them.)
3. **Timer:** GitHub only runs cron from the default branch, so use cron-job.org (a second job next to the main bot's):
   - URL: `https://api.github.com/repos/hitechparadigm/community-ai-autoposter/actions/workflows/tick.yml/dispatches`
   - Method POST, every 5 minutes, body `{"ref":"ManitobaBotNews"}`
   - Headers: `Authorization: Bearer <token with Actions: write>`, `Accept: application/vnd.github+json`
4. **First run:** Actions → "Draft posts" → Run workflow, choose branch `ManitobaBotNews`. Read the log for `FEED ERROR` lines
   and fix or remove those feeds in `config.py`.

## Notes
- "This day" posts appear only on days when Wikipedia's "On this day" has a Manitoba-related entry.
- Referrals, community-news priority and the Sunday community-history column are switched off.
- Merging `main` into this branch will conflict in `config.py`, `prompts.py`, `state.json`; keep this branch's versions.
