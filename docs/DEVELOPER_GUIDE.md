# Developer guide

How the code works, for anyone who wants to read, change or extend it. For using the bot as an approver, see the
[guide for approvers](USER_GUIDE.md); for setup, the [README](../README.md).

## The big picture

The bot is a set of short **jobs** that GitHub Actions runs. It has no server and no database:

- A free timer (cron-job.org) starts the **tick** every 5 minutes (`.github/workflows/tick.yml`). The tick runs
  whatever is due by `SCHEDULE` in `community/config.py`, then reads Telegram for approvers' taps and messages.
- Each job reads the bot's **memory** (`state.json`), does its work and saves the memory back. The memory lives in
  a private `<repo>-state` repository; `save_state.sh` commits it after every run.
- **Claude** (Anthropic's model) does all the writing and judging through one function, `ask_claude`.
- Nothing is published until an approver taps ✅ in Telegram (unless `AUTO_PUBLISH` is switched on).

The repository has three parts:

| Folder | What it is | Who changes it |
| --- | --- | --- |
| `community/` | Everything specific to one community: settings, editorial prompts, glossary, card design | Anyone running their own channel |
| `autoposter/` | The program: no names, sources or languages inside | Developers |
| `.github/workflows/` | When and how jobs run on GitHub Actions | Developers |

`bot.py` is only the command line: `python3 bot.py tick`, `python3 bot.py draft`, and so on (`python3 bot.py` with
no command lists them all).

## The modules

Each module imports only from the ones above it in this table, so there are no import cycles:

| Module | Job | Main functions |
| --- | --- | --- |
| `core.py` | Settings from the environment, time, HTTP, the bot's memory, Telegram calls | `http`, `tg`, `load_state`, `save_state`, `merge_state` |
| `sources.py` | News feeds and searches, article pages, photos, Wikipedia | `fetch_news`, `parse_feed`, `fetch_page`, `commons_image`, `wiki_text` |
| `ai.py` | Claude calls and the checks around writing | `ask_claude`, `review_post`, `edit_ok`, `parse_post`, `glossary_for` |
| `cards.py` | Facebook picture cards from `community/card.html` | `render_card`, `make_card` |
| `channels.py` | Destinations: Telegraph, Facebook, the Telegram post format | `telegraph`, `post_to_facebook`, `fb_text`, `format_post` |
| `drafts.py` | Drafts for approval, publishing, daily counts, the learning log | `send_draft`, `publish_draft`, `close_draft`, `learn` |
| `news.py` | News, 💡 Варто знати and the morning digest | `cmd_draft`, `_draft_item`, `cmd_digest` |
| `history.py` | 📅 This day and 🍁 history long-reads | `cmd_thisday`, `cmd_history`, `_write_history` |
| `research.py` | 🔎 Розбираємося: an article on a topic from web search | `research_topic`, `find_sources` |
| `learning.py` | Reader comments, reactions, the monthly review and production numbers | `cmd_review`, `record_comment`, `cmd_stats` |
| `evals.py` | The evaluation set: test posts, checks, judge, scorecard | `cmd_eval`, `score`, `judge` |
| `approval.py` | What approvers send: taps, feedback replies, ideas | `cmd_approve`, `handle_feedback`, `handle_idea` |
| `cli.py` | The tick and the other commands | `cmd_tick`, `main` |

Every function has a short docstring saying what it does; start from the main functions above.

## Life of a news post

1. **Tick** (`cli.cmd_tick`): it's 12:00 and `news` is due, so it calls `news.cmd_draft()`. The schedule key is
   saved first, so a crash can't make the same draft twice.
2. **Gather** (`sources.fetch_news`): read every feed in `FEEDS`, keep recent stories the bot hasn't offered before
   (`state["seen"]`), Ukrainian-community stories first.
3. **Pick** (`ask_claude` with `PICK_PROMPT`): Claude returns the id of the best story.
4. **Write** (`news.write_news`, called by `news._draft_item`): fetch the article; Claude writes title, body, a topic emoji and photo searches
   (`WRITE_PROMPT`). The article is sent once as a cached block and reused by the next steps.
5. **Copy-edit** (`EDIT_PROMPT`), then `ai.edit_ok` rejects a version that came back cut short or garbled.
6. **Review** (`ai.review_post`): a separate Claude call checks the draft against the article, fixes it once and
   checks again; anything left is shown to approvers as a ⚠️ note.
7. **Send** (`drafts.send_draft`): the draft goes to every approver with ✅/❌ buttons and the daily count; if
   Facebook is set up, `cards.make_card` draws the picture card and sends it too. The draft is stored in
   `state["pending"]`.
8. **Approve** (next tick, `approval.cmd_approve`): Telegram reports the tap, a reply "опублікувати"
   (`PUBLISH_WORDS`, `approval.handle_feedback`) or a 👍 reaction (`PUBLISH_REACTIONS`, `approval.handle_reaction`)
   on the draft or its card. All three go through `approval.decide`: `drafts.publish_draft` posts to the channel,
   then `channels.post_to_facebook` posts the card and text and adds the first comment. Approvers' copies are
   updated, the count goes up, and the event is logged for the monthly review.

A topic sent without a link goes to `research.research_topic`:
1. `research.find_sources`: `ai.claude_search` lets Claude search the web with Anthropic's web search tool and
   list the best pages (`RESEARCH_SEARCH_PROMPT`). If that tool is unavailable, the bot falls back to the search
   feeds in `RESEARCH` (`sources.web_search`) and lets Claude pick from the results.
2. `research._read_pages` reads them with the bot's own reader; pages it can't load (PDFs, slow or
   script-blocking sites) are read in one call through Anthropic's web fetch tool (`ai.claude_fetch`).
3. A coverage check (`RESEARCH_COVERAGE_PROMPT`) asks whether the pages answer the request; if not, one more
   search for what is missing. With fewer than `min_sources` readable pages, `NotCovered` is raised and the
   approver is told what's missing; otherwise the gaps go to the writer, who must say plainly what isn't covered.
4. The pages are numbered as one source text; the article is written (`RESEARCH_WRITE_PROMPT`), copy-edited and
   reviewed (with `RESEARCH_REVIEW_NOTE`), then published on Telegraph with the list of sources. The draft keeps
   its `topic`, so a feedback reply researches and writes it again.

History long-reads follow the same path, but are written by `history._write_history`, published as a Telegraph
page, and the channel gets a teaser with a "Read more" link.

## Where Claude is called

Almost all calls go through `ai.ask_claude(prompt, source=None, schema=None)` (the exceptions are
`ai.claude_search` and `ai.claude_fetch`, which use Anthropic's web search and web fetch tools for 🔎 articles):

- **`source`**: the article text, sent first with prompt caching, so the writer, editor and reviewer read it from
  the cache instead of paying for it again. Prompts refer to it as `SOURCE_REF`.
- **`fast=True`**: a simple choice (picking stories, search queries, titles, comment gists, the digest shortlist)
  goes to `config.FAST_MODEL` (Haiku) instead of `config.MODEL` (Sonnet). Anything readers will see stays on
  `MODEL`. Each call's tokens are priced by its model (`config.PRICES`) and the run's total is printed at the end.
- **`schema`**: when given, Claude answers through a tool with that JSON schema, so the answer is always
  well-formed. Schemas are defined in `ai.py` (`SCHEMA_IDS`, `SCHEMA_REVIEW`, …).
- **Added automatically:** the matching entries of `community/glossary.json` (only names that appear in the text)
  and the editorial notes approvers accepted in the monthly review. Story picking gets neither.

The prompts themselves are in `community/prompts.py`; `STYLE` (the Ukrainian style guide) is part of every writing
prompt.

## The bot's memory (state.json)

| Key | What it holds |
| --- | --- |
| `seen` | Story links already offered (one week), so they aren't offered again |
| `pending` | Drafts waiting for approval: text, approvers' message ids (`msgs`, and `card_msgs` for the card), Facebook card file id and spec, kind; long-reads also their Telegraph path, 🔎 articles their `topic` |
| `tg_offset` | The next Telegram update to read |
| `schedule_done` | Scheduled jobs already run (one week) |
| `history_done` | History sources already used |
| `digest_regions`, `ref_index`, `ref_news` | Rotation of digest regions and referral links |
| `published_log` | Posts published per day and kind (for the daily counts) |
| `learn` | Published, skipped, feedback and idea events (120 days) for the monthly review |
| `tg_reactions`, `tg_comments`, `tg_comment_count` | Readers' reactions, and anonymous gists of constructive comments |
| `lessons_pending`, `editorial_notes` | Rules proposed by the monthly review, and the ones approvers accepted |

When two runs save at the same time, `save_state.sh` calls `core.merge_state`, a three-way merge that keeps both
runs' changes. A tap is confirmed to Telegram as soon as it is read, so overlapping runs never publish twice.

## Common changes

- **Add a news source:** add `(name, feed URL, region)` to `FEEDS` in `community/config.py`. Test it first with
  the Check connections workflow (it can try new feeds).
- **Add a scheduled post type:** write a `cmd_…` function (copy `news.cmd_draft` as a model), add it to `jobs` in
  `cli.cmd_tick`, its times to `SCHEDULE`, and its labels to `LABELS` and `KIND_NAMES`.
- **Change how posts are written:** edit `community/prompts.py`. A wrong institution name usually belongs in
  `community/glossary.json` instead.
- **Add a destination** (another network): add a `post_to_…` function in `channels.py` and call it from
  `drafts.publish_draft`, the way Facebook is called.
- **Change the card design:** edit `community/card.html` (and `CARD` in `community/config.py`: brand, tagline,
  call to action, fallback photos), then run the Preview Facebook cards workflow. `cards.make_card` looks for a
  photo in this order: the card's `queries` (Wikimedia Commons, Commons-hosted files only), then
  `CARD["fallback_photos"]` for the card's kind; it records the card's message ids (`card_msgs`) so replies and
  👍 on the card work like on the draft.

## Evaluation

Tests check the code; the evaluation set checks the writing. `evals/cases.json` holds fictional test stories,
each with what a good post must contain. `python3 bot.py eval` (or Actions → Evaluation) writes a post from
each with `news.write_news`, the same function real drafts use, then:

- `evals.score` runs the automatic checks (facts, glossary names, people's original names, untranslated
  organization names, forbidden words from `EVAL` in `community/config.py`, form, reviewer verdict);
- `evals.judge` asks a separate Claude call to grade accuracy, language and usefulness from 1 to 5;
- the scorecard goes to `evals/results/latest.md` and `latest.json`, and a full run adds a line to
  `history.csv` with the prompts' fingerprint and cost, so runs can be compared.

The workflow runs by itself when `community/prompts.py`, `community/glossary.json` or the cases change, and
commits the results. A run costs about $0.60. To add a case, copy one in `cases.json`; facts are regular
expressions matched against the post with numbers written one way (`40 000` and `40,000` both become `40000`).
Keep cases fictional: real articles are copyrighted.

## Tests

```
python3 -m unittest discover -s tests -v
```

`tests/test_evals.py` covers the evaluation checks; `tests/test_core.py` covers parsing, merging, writing checks, Facebook text, cards, counts and approvers'
messages; `tests/test_flow.py` runs a whole draft → approval → publish cycle with the network faked. They run on
GitHub on every code change (`tests.yml`) and need no keys or packages. Add a test with every fix.

## Conventions

- Standard library only: no `pip install`, so GitHub Actions starts in seconds.
- No community-specific words in `autoposter/`: they go in `community/config.py` (`LABELS`) or the prompts.
- Secrets only in environment variables (GitHub secrets); the code never prints them.
- Readers' personal data is never stored: comments are reduced to anonymous gists.
- Every function has a docstring; comments explain *why*, not *what*.
