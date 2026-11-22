# Ukrainian Canada autoposter (step 1: Telegram)

Five times a day (9:00-21:00) it reads Canadian news feeds, has Claude pick the most relevant story and
write short posts in Ukrainian, and sends them to you in Telegram with **✅ Publish / ❌ Skip**
buttons. Posts you approve go to @UkrainianCanada within about 30 minutes.

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

## Morning digest

Every morning at 6:30 Toronto time you get a "🗞 Головне за вчора" draft: the 3-5 most important Canadian
stories from yesterday, 1-2 stories from 3-4 provinces or territories (rotating, so every region gets
featured over the week), and "📌 Сьогодні": up to 3 things the news says happen today (a strike starting,
a deadline, a vote). That section is left out when the news mentions nothing for today. A key phrase in each
item links to the source article, outlets are mixed (CBC, Global News, Postmedia papers), and the post ends
with "За матеріалами: ...".

News drafts come at 9:00, 12:00, 15:00, 18:00 and 21:00; "This day" at 8:30; the history story at 11:30.

## Facebook Page

When the secrets `FACEBOOK_PAGE_ID` and `FACEBOOK_PAGE_TOKEN` are set, every post you approve is also
published to the Facebook Page (as plain text with the link card; long-reads link to the Telegraph article).
Without them, only Telegram is used. If Facebook fails, the Telegram post still goes out and the draft says
"Facebook failed".

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

History posts are long-reads on Telegraph (telegra.ph), which open inside Telegram with Instant View.
The channel gets a teaser with a photo and a "📖 Читати повністю" link. The bot creates its own Telegraph
account automatically (token kept in `state.json`); a skipped or expired draft's page is blanked.

Two extra drafts a day, approved the same way. Canadian sources come first; Wikipedia is only a
fallback. Posts show a photo above the text: the source's own picture, or, if it has no real photo
(only a logo or banner), a freely licensed photo of the subject from Wikimedia Commons.

- **📅 Цей день в історії Канади** (8:30 Toronto time): alternates between an event that happened on
  today's date and a person born or died on it. People come from the Dictionary of Canadian Biography;
  events from Wikipedia "On this day" (Canadian entries), because the Canadian sites with dated events
  block automated access.
- **🍁 Історія Канади** (11:30): a story chosen from `HISTORY_SOURCES` in `config.py`: CBC Archives,
  Library and Archives Canada, Ontario Heritage Trust, Quebec Anglophone Heritage Network, Manitoba
  Historical Society, Encyclopedia of Saskatchewan, RETROactive Alberta (fallback and coverage for BC,
  the Atlantic provinces and the North: `WIKI_REGIONAL_TOPICS`).
- **Sundays:** a Ukrainian-Canadian story from `UKRAINIAN_CANADIAN_SOURCES` (Library and Archives
  Canada, RETROactive Alberta, the Internment Recognition Fund; fallback: `UKRAINIAN_CANADIAN_TOPICS`).
  To get one on another day: Actions → "Draft history story" → tick "Ukrainian-Canadian story".
