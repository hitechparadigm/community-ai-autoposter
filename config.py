# Settings for the Ukrainian Canada autoposter. Edit freely.

# Telegram channel where approved posts go
CHANNEL = "@UkrainianCanada"

# News sources: (display name, RSS/Atom feed URL)
# If a feed stops working, the run log shows "FEED ERROR" and the rest still run.
FEEDS = [
    ("CBC News", "https://www.cbc.ca/webfeed/rss/rss-canada"),
    ("CBC Manitoba", "https://www.cbc.ca/webfeed/rss/rss-canada-manitoba"),
    ("Global News", "https://globalnews.ca/canada/feed/"),
    ("Ukrinform", "https://www.ukrinform.net/rss/block-lastnews"),
]

# Drafts each run sends you (it may send fewer). 5 runs a day x 1 = up to 5 posts/day.
# Set to 2 to get a backup option each run.
DRAFTS_PER_RUN = 1

# Ignore news older than this
MAX_AGE_HOURS = 36

# Drafts not approved within this time are dropped
DRAFT_EXPIRY_HOURS = 24

# Claude model used to pick, write and copy-edit posts (Sonnet 5.5)
MODEL = "claude-sonnet-5-5"

# ---------- Canadian history ----------
# "📅 Цей день в історії Канади" (daily): an event on today's date (Wikipedia "On this day")
#   or the Dictionary of Canadian Biography's person of the day.
# "🍁 Історія Канади" (daily): a story picked from the sources below.
# On this weekday (0 = Monday ... 6 = Sunday) it tells a Ukrainian-Canadian story instead.
UKRAINIAN_CANADIAN_DAY = 6

# English Wikipedia article titles for Ukrainian-Canadian Sundays, used in order.
UKRAINIAN_CANADIAN_TOPICS = [
    "Ivan Pylypiw",
    "Wasyl Eleniak",
    "Ukrainian Canadian internment",
    "Ukrainian Canadian Congress",
    "Ray Hnatyshyn",
    "Vegreville egg",
    "Ukrainian Cultural Heritage Village",
    "Ukrainian Canadians",
    "Canadian Ukrainian Catholic Church",
]

# Story sources. Each run samples a few of them, collects article links from a random index page,
# and Claude picks the most interesting story. In "index", {n} = random page number up to "pages",
# {letter}/{LETTER} = random letter. "pattern" decides which links count as articles.
# All of these were checked to be readable from GitHub.
HISTORY_SOURCES = [
    {"name": "CBC Archives", "region": "Canada",
     "index": ["https://www.cbc.ca/archives/history", "https://www.cbc.ca/archives"],
     "pattern": r"cbc\.ca/archives/[a-z0-9-]+-1\.\d+$"},
    {"name": "Library and Archives Canada", "region": "Canada",
     "index": ["https://thediscoverblog.com/page/{n}/"], "pages": 60,
     "pattern": r"thediscoverblog\.com/\d{4}/\d{2}/\d{2}/[a-z0-9-]+/$"},
    {"name": "Ontario Heritage Trust", "region": "Ontario",
     "index": ["https://www.heritagetrust.on.ca/sitemaps-1-section-articles-1-sitemap.xml"],
     "pattern": r"heritagetrust\.on\.ca/heritagematters/articles/[a-z0-9-]+$"},
    {"name": "Quebec Anglophone Heritage Network", "region": "Quebec",
     "index": ["https://qahn.org/article?page={n}"], "first_page": 0, "pages": 20,
     "pattern": r"qahn\.org/article/[a-z0-9-]+$"},
    {"name": "Manitoba Historical Society", "region": "Manitoba",
     "index": ["https://www.mhs.mb.ca/docs/people/index_{letter}.shtml"],
     "pattern": r"mhs\.mb\.ca/docs/people/[a-z][a-z0-9]*_[a-z0-9_]+\.shtml$"},
    {"name": "Encyclopedia of Saskatchewan", "region": "Saskatchewan",
     "index": ["https://esask.uregina.ca/entry_list-l={LETTER}.html"],
     "pattern": r"esask\.uregina\.ca/entry/[a-z0-9_]+\.html$"},
    {"name": "RETROactive: Alberta's Historic Places", "region": "Alberta",
     "index": ["https://albertashistoricplaces.com/category/subject/albertas-history-subject/page/{n}/"],
     "pages": 25, "pattern": r"albertashistoricplaces\.com/\d{4}/\d{2}/\d{2}/[a-z0-9-]+/$"},
]

# Regions without a source that GitHub can read (sites that block bots or need JavaScript):
# well-known topics from English Wikipedia. Add your own: ("Region", "Article title").
WIKI_REGIONAL_TOPICS = [
    ("British Columbia", "Komagata Maru incident"),
    ("British Columbia", "Cariboo Gold Rush"),
    ("British Columbia", "Last Spike (Canadian Pacific Railway)"),
    ("Nova Scotia", "Halifax Explosion"),
    ("Nova Scotia", "Bluenose"),
    ("Nova Scotia", "Pier 21"),
    ("New Brunswick", "Expulsion of the Acadians"),
    ("New Brunswick", "Saint John, New Brunswick"),
    ("Prince Edward Island", "Charlottetown Conference"),
    ("Prince Edward Island", "Anne of Green Gables"),
    ("Newfoundland and Labrador", "L'Anse aux Meadows"),
    ("Newfoundland and Labrador", "Newfoundland Railway"),
    ("Newfoundland and Labrador", "Beothuk"),
    ("Yukon", "Klondike Gold Rush"),
    ("Yukon", "Alaska Highway"),
    ("Northwest Territories", "Franklin's lost expedition"),
    ("Northwest Territories", "Mackenzie River"),
    ("Nunavut", "Nunavut Land Claims Agreement"),
    ("Nunavut", "Inuit"),
]
