# Settings for the Manitoba News bot. Edit freely.
# This branch (ManitobaBotNews) is a Manitoba-only, English-language version of the autoposter.

# Telegram channel where approved posts go (the bot must be an admin of this channel)
CHANNEL = "@ManitobaBotNews"

# How the bot identifies itself to websites that ask for it (Wikipedia, Telegraph)
BOT_NAME = "ManitobaBotNews"
BOT_CONTACT_URL = "https://t.me/ManitobaBotNews"

# Local time zone (daylight saving time is handled automatically)
TIMEZONE = "America/Winnipeg"

# When each kind of draft is made, in local time. A job that GitHub starts late still runs if it is
# less than CATCH_UP_HOURS late. Approved posts are published every 5 minutes, around the clock.
SCHEDULE = {
    "digest": ["06:30"],
    "thisday": ["08:30"],
    "news": ["09:00", "12:00", "15:00", "18:00", "21:00"],
    "history": ["11:30"],
}
CATCH_UP_HOURS = 2

# Fixed words in posts, in the channel's language
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
LABELS = {
    "source": "Source",
    "photo": "Photo",
    "read_more": "Read the full story",
    "wikipedia": "Wikipedia",
    "digest_title": "Manitoba news digest",
    "digest_national": "🍁 Top stories",
    "digest_community": "🏘 Community",
    "digest_today": "Today",
    "digest_sources": "Sources",
    "thisday_header": "📅 This day in Manitoba history",
    "history_header": "🌾 Manitoba history",
    "auto_publish_note": "Will be published automatically at {time} unless you tap ❌",
    "unpublished": "This article was not published",
    "review_warning": "The review found problems, please check carefully",
}

# News sources: (display name, RSS/Atom feed URL, region)
# If a feed stops working, the run log shows "FEED ERROR" and the rest still run.
# CBC Manitoba and Global News Winnipeg are the same feeds the original bot uses (known to work from GitHub).
# The others follow each outlet's usual feed address; check the first run's log for "FEED ERROR" and
# remove or fix any that fail.
FEEDS = [
    ("CBC Manitoba", "https://www.cbc.ca/webfeed/rss/rss-canada-manitoba", "Manitoba"),
    ("Global News Winnipeg", "https://globalnews.ca/winnipeg/feed/", "Manitoba"),
    ("Winnipeg Sun", "https://winnipegsun.com/feed/", "Manitoba"),
    ("CityNews Winnipeg", "https://winnipeg.citynews.ca/feed/", "Manitoba"),
    ("Winnipeg Free Press", "https://www.winnipegfreepress.com/rss/?path=%2Flocal", "Manitoba"),
    ("Brandon Sun", "https://www.brandonsun.com/rss/?path=%2Flocal", "Manitoba"),
]

# This bot has no "community" priority: nothing is marked or preferred as community news.
COMMUNITY_REGIONS = ()
NOT_COMMUNITY_REGIONS = ()
DIGEST_EXCLUDE_REGIONS = ()

# Outlet names used in "sources" lines: feed names starting with these are shortened to them
OUTLET_PREFIXES = ("CBC", "Global News", "CityNews", "Winnipeg Free Press")
# Tracking bits removed from links in Facebook posts
STRIP_FROM_LINKS = ("?cmp=rss",)

# Newest items taken from each feed per run (keeps big feeds from crowding out small ones).
ITEMS_PER_FEED = 10
COMMUNITY_WORDS = ()

# Drafts each run sends you (it may send fewer). 5 runs a day x 1 = up to 5 posts/day.
# Set to 2 to get a backup option each run.
DRAFTS_PER_RUN = 1

# Ignore news older than this
MAX_AGE_HOURS = 36

# Drafts not approved within this time are dropped
DRAFT_EXPIRY_HOURS = 24

# Publishing without approval, per kind of post. True = the draft is published automatically after
# AUTO_PUBLISH_AFTER_MINUTES unless an approver taps ❌ (✅ still publishes it right away).
# False = it waits for ✅.
AUTO_PUBLISH = {
    "news": False,      # news posts (up to 5 a day)
    "digest": False,    # morning digest
    "thisday": False,   # 📅 This day in Manitoba history
    "history": False,   # 🌾 Manitoba history long-reads
}
AUTO_PUBLISH_AFTER_MINUTES = 60

# Daily digest (python bot.py digest): top Manitoba stories plus 3-4 areas of the province, rotating
DIGEST_NATIONAL = "3-5"
DIGEST_REGIONS = "3-4"

# Referral links: none for this channel. (Add (text, link, what it is) tuples to turn them on.)
REFERRALS = []
REFERRALS_IN_NEWS_PER_DAY = 0
REFERRAL_DISCLOSURE = ""

# Claude model used to pick, write and copy-edit posts (Sonnet 5.5)
MODEL = "claude-sonnet-5-5"

# ---------- Manitoba history ----------
# History posts are long-reads on Telegraph (telegra.ph, opens inside Telegram); the channel gets a teaser.
TELEGRAPH_AUTHOR = "Manitoba News"
TELEGRAPH_AUTHOR_URL = "https://t.me/ManitobaBotNews"

# No separate community-history day: -1 never matches a weekday (0 = Monday ... 6 = Sunday).
COMMUNITY_HISTORY_DAY = -1
COMMUNITY_HISTORY_LABEL = "Manitoba communities"
COMMUNITY_HISTORY_SOURCES = []
COMMUNITY_HISTORY_TOPICS = []

# Story sources for the history column. Each run samples from these, collects article links from a random
# index page, and Claude picks the most interesting story. In "index", {letter} = random letter.
HISTORY_SOURCES = [
    {"name": "Manitoba Historical Society", "region": "Manitoba",
     "index": ["https://www.mhs.mb.ca/docs/people/index_{letter}.shtml"],
     "pattern": r"mhs\.mb\.ca/docs/people/[a-z][a-z0-9]*_[a-z0-9_]+\.shtml$"},
]

# "This day": there is no Manitoba-only "person of the day" page, so only Wikipedia's "On this day"
# is used, with entries that mention one of THISDAY_WORDS. On days without a match, no draft is made.
PEOPLE_OF_THE_DAY = None
WIKIPEDIA_LANG = "en"
THISDAY_WORDS = ("Manitoba", "Winnipeg", "Brandon", "Red River", "Métis", "Metis", "Louis Riel", "Selkirk",
                 "Churchill", "Portage la Prairie", "Steinbach", "Thompson", "Flin Flon", "Dauphin",
                 "Assiniboine", "Lake Winnipeg", "Fort Garry", "The Forks", "Winnipeg Jets",
                 "Blue Bombers", "Hudson's Bay")

# Wikipedia fallback when the sources above give nothing usable, and the main coverage for topics the
# history sites can't be read for. Add your own: ("Manitoba", "Article title").
WIKI_REGIONAL_TOPICS = [
    ("Manitoba", "Red River Rebellion"),
    ("Manitoba", "Louis Riel"),
    ("Manitoba", "Manitoba Act"),
    ("Manitoba", "Winnipeg general strike"),
    ("Manitoba", "Seven Oaks massacre"),
    ("Manitoba", "Red River Colony"),
    ("Manitoba", "1950 Red River flood"),
    ("Manitoba", "Red River Floodway"),
    ("Manitoba", "Manitoba Schools Question"),
    ("Manitoba", "Women's suffrage in Manitoba"),
    ("Manitoba", "Nellie McClung"),
    ("Manitoba", "Lower Fort Garry"),
    ("Manitoba", "Upper Fort Garry"),
    ("Manitoba", "York Factory"),
    ("Manitoba", "Prince of Wales Fort"),
    ("Manitoba", "The Forks, Winnipeg"),
    ("Manitoba", "Manitoba Legislative Building"),
    ("Manitoba", "Winnipeg Falcons"),
    ("Manitoba", "Canadian Museum for Human Rights"),
    ("Manitoba", "Riding Mountain National Park"),
    ("Manitoba", "Churchill, Manitoba"),
    ("Manitoba", "Mennonites in Manitoba"),
    ("Manitoba", "Icelandic Canadians"),
    ("Manitoba", "Treaty 1"),
    ("Manitoba", "Winnipeg Free Press"),
    ("Manitoba", "Assiniboine Park Zoo"),
    ("Manitoba", "Portage la Prairie"),
    ("Manitoba", "Brandon, Manitoba"),
    ("Manitoba", "Flin Flon"),
    ("Manitoba", "Dauphin, Manitoba"),
]
