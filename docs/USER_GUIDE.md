# Ukrainian Canada News bot — guide for approvers

Last updated: November 2026. For how it is built and set up, see the [README](../README.md).

## What the bot does

The bot writes posts in Ukrainian, sends each one to us as a draft in the chat with **Ukrainian Canada News** (@UkrainianCanadaPostBot), and publishes it only when one of us taps **✅ Publish**.

- **Where approved posts go:** the Telegram channel [@UkrainianCanada](https://t.me/UkrainianCanada) and the Facebook Page [Ukrainian Canada - Українська Канада](https://www.facebook.com/canadaua). Long history stories also get a full article on Telegraph.
- **Where stories come from:** about 60 Canadian sources: CBC, Global News and CTV News for every province and territory, Postmedia papers, New Pathway, UCC, the Canada-Ukraine Foundation, Ukrainian churches, and news searches for Ukrainian-Canadian stories in any outlet. History comes from Canadian archives first, Wikipedia only as a fallback.
- **Who writes:** Claude, an AI model. A second pass copy-edits the Ukrainian and checks facts, and a reviewer compares the result with the original article before we see it.
- **Nothing is posted without us.** Every approver gets every draft; whoever taps first decides, and the other copies update to show who did.

## Daily schedule

Drafts arrive at these times (Toronto time), 9 a day, plus a monthly report:

| Time | Draft |
| --- | --- |
| 6:30 | 🗞 Morning digest: yesterday's main news, 3-4 provinces, the Ukrainian community, what's on today |
| 8:30 | 📅 Цей день в історії Канади: an event or a person on today's date |
| 9:00, 12:00, 15:00, 18:00, 21:00 | News post, Ukrainian-community stories first |
| 11:30 | 🍁 Історія Канади long-read (Sundays: the history of Ukrainians in Canada) |
| 19:30 | 💡 Варто знати: a practical story with tips |
| 1st of the month, 10:00 | 📈 Monthly review: a report and proposed rules |

A draft that nobody taps expires after 24 hours.

## Approving a draft

Each draft arrives as a message with two buttons, followed by a separate **🖼 Facebook** picture: the card that will go on Facebook.

1. Read the draft. Open the link at the bottom if you want to check the original article.
2. Tap **✅ Publish** or **❌ Skip**. The bot checks for taps every 5 minutes, so publishing can take up to 5 minutes. When it's done, the draft shows "✅ Published by … + Facebook".
3. If the buttons are still there 5 minutes after tapping, the tap didn't reach the bot (this happens when the app is briefly offline). Two other ways that always work:
   - **Reply** to the draft or its Facebook card with **опублікувати** (or publish, так, ok, 👍); reply **пропустити** (or skip, ❌) to skip it.
   - Put a **👍 reaction** on the draft or its card to publish it.

Things you'll see on drafts (they are for us only and are never published):

- **📊 Сьогодні опубліковано новин: 4 з 5** — how many posts of that kind went out today against the daily plan (5 news, 1 of each other kind). Going over is allowed; it is marked ⚠️.
- **⚠️ Перевірка знайшла проблеми…** — the reviewer flagged something it couldn't fix (an unsupported fact, repetition, awkward language). Read those drafts carefully, fix them with a reply (next section), or skip them.

Auto-publishing is switched off: nothing goes out unless someone taps ✅.

## Asking for changes

If a draft needs changes, **reply to it** (swipe left on the draft, or long-press → Reply) and write what to change, in Ukrainian or English. For example:

- "коротше"
- "прибери останній абзац"
- "не перекладай назву організації"
- "зроби заголовок про Манітобу"

The bot answers "✍️ Переписую…" and within about 5 minutes sends a new version with new buttons and a new Facebook card. The old draft is marked "✏️ Переписано…". You can reply to the new version again if needed.

News, Варто знати and the digest are edited in place: links stay the same and facts are checked against the original article. History long-reads are written again from their source, following your note. If a rewrite fails, the bot says so and the old draft stays as it was.

## Suggesting your own posts

Send the bot a normal message (not a reply to a draft) and it prepares a draft from it within about 5 minutes:

| You send | You get |
| --- | --- |
| A link to an article | A news draft from that article |
| A link + a note, e.g. "https://… зроби акцент на українцях" | A news draft that follows the note |
| "історія" + a topic, e.g. "історія Банф" | A history long-read on that topic |
| "історія" + a link | A history long-read from that page |
| "варто знати" + a link | A practical story with tips |
| /help | A reminder of these options |

A news idea without a link gets a reply asking for one: news posts are always based on a real article.

To publish your own finished text, use **Draft from your own text** in GitHub (see the last section).

## What each post looks like

| Post | In the Telegram channel |
| --- | --- |
| News | Topic emoji + headline, 2-3 short paragraphs, "🔗 Джерело" link |
| 💡 Варто знати | A short real story, then "Що можна зробити:" with 3-4 tips |
| 🗞 Digest | National news, 3-4 provinces, the community, today; each item links to its outlet; one referral link at the end |
| 📅 Цей день / 🍁 Історія | A short teaser with "📖 Читати повністю": the full article opens on Telegraph, with a photo |

**On Facebook** every approved post goes out automatically in a Facebook format:

- a picture card (photo on top, headline below) instead of a link preview;
- the full text, with no links, because Meta blocks Canadian news links in Canada; sources are named in plain text;
- an automatic first comment with the link to our Telegram channel, and for long-reads the Telegraph article;
- no referral links.

Facebook groups can't be posted to automatically (Meta closed that). To post in the group, open the post on the Page → **Share → Share to a group**. Share only 1-3 a day: the digest, community news, the history story.

If a channel post needs a fix after publishing, edit it in Telegram (long-press → Edit) and on Facebook (… → Edit post).

## Quality and learning

- **Style rules:** literary Ukrainian, no russianisms or calques. People's names in Ukrainian with the original in brackets on first mention: Марі Томпсон (Marie Thompson). Companies, charities and community groups keep their English or French name (Open Harbour Refugee Association). Government bodies, Ukrainian organizations and public institutions such as museums, universities and hospitals get a Ukrainian name with the original in brackets: міністерство імміграції Канади (IRCC), Конгрес українців Канади (КУК), Університет Макгілла (McGill University).
- **Glossary:** a list of established names (CSIS = Канадська служба безпеки й розвідки, могавки, метиси…) that the bot must use. When you spot a wrong name, tell the bot's maintainer and it goes into the glossary ([glossary.json](../community/glossary.json)), so the mistake doesn't repeat.
- **Monthly review:** the bot records what we publish, skip, ask to change and suggest, plus how readers react: Telegram reactions and comments, Facebook reactions, comments and shares. On the 1st of each month it sends us a short report and proposes a few rules for future posts. The rules apply only if one of us taps ✅. Emotional and off-topic comments are ignored, and readers' words are never stored, only an anonymous summary of useful ones.

So the more feedback we give through replies, the better the posts get.

## Manual tools and help

Most of the time Telegram is all you need. For extra tools, there are buttons in [GitHub → Actions](https://github.com/hitechparadigm/community-ai-autoposter/actions) (pick one → **Run workflow**; you need to be a collaborator on the repository):

| Tool | Use it to |
| --- | --- |
| Draft posts | Get a news draft now (tick "Варто знати" for a practical story) |
| Draft morning digest / Draft this-day post / Draft history story | Get those drafts now; history can also be written from a link or Wikipedia article you give |
| Draft from your own text | Turn your own finished text into a draft with a Facebook card |
| Publish approved posts | Publish what was approved right away, instead of waiting up to 5 minutes |
| Rewrite a published long-read | Fix a published Telegraph article in place |
| Check connections | Test that Telegram, Facebook and all news feeds work (posts nothing) |

If something looks wrong (taps do nothing for more than 10 minutes, posts are missing on Facebook, drafts stop arriving), message the bot's maintainer with a screenshot.
