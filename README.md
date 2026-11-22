# Ukrainian Canada autoposter (step 1: Telegram)

Five times a day it reads Canadian news feeds, has Claude pick the most relevant story and
write short posts in Ukrainian, and sends them to you in Telegram with **✅ Publish / ❌ Skip**
buttons. Posts you approve go to @UkrainianCanada within about 20 minutes.

## Setup (one time, easiest from a computer)

1. **Create a private GitHub repo** (e.g. `ukrainiancanada-autopost`) and upload all these files,
   keeping the `.github/workflows` folder structure.
2. **Get your Telegram user ID:** message @userinfobot in Telegram; it replies with your numeric ID.
3. **Open a chat with your bot** and press Start (otherwise it can't message you).
4. **Make the bot a channel admin** of @UkrainianCanada with "Post messages" on.
5. **Add secrets:** repo → Settings → Secrets and variables → Actions → New repository secret:
   - `ANTHROPIC_API_KEY` – from console.anthropic.com
   - `TELEGRAM_BOT_TOKEN` – from @BotFather
   - `TELEGRAM_ADMIN_ID` – your numeric ID from step 2. For several approvers, separate IDs with commas: `456360947,123456789`
6. **Test:** Actions tab → "Draft posts" → Run workflow. Drafts should arrive in Telegram
   within a minute. Tap ✅ on one, then run "Publish approved posts" by hand to post right away.

## Changing things

Edit `config.py`: news sources, drafts per run, model. Run times are in the `cron:` lines
of the two workflow files (times are UTC).

## Notes

- Posts are summaries in Claude's own words with a link to the source; Telegram shows the
  article's preview image from the link.
- If a feed breaks, the run log shows `FEED ERROR` and the other feeds still work.
- `state.json` remembers which stories were already offered and is updated automatically.
- GitHub pauses scheduled workflows in a repo with no activity for 60 days; if that happens,
  re-enable them in the Actions tab.

## Canadian history

Two extra drafts a day, approved the same way:

- **📅 Цей день в історії Канади** (8:30 Toronto time): something that happened on today's date,
  from Wikipedia "On this day" (Canadian entries) or the Dictionary of Canadian Biography's
  person of the day (born or died on this date).
- **🍁 Історія Канади** (11:30): a story chosen from the sources in `config.py`
  (`HISTORY_SOURCES`: CBC Archives, Library and Archives Canada, Ontario Heritage Trust, Quebec
  Anglophone Heritage Network, Manitoba Historical Society, Encyclopedia of Saskatchewan,
  RETROactive Alberta) plus Wikipedia topics for the other provinces and territories
  (`WIKI_REGIONAL_TOPICS`). On Sundays it tells a Ukrainian-Canadian story
  (`UKRAINIAN_CANADIAN_TOPICS`).

Run either any time from the Actions tab.
