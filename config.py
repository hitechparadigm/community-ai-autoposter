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

# ---------- Canadian history column ----------
# One history draft a day (see .github/workflows/history.yml for the time).
# Most days: a Canadian story that happened on this date (from Wikipedia "On this day").
# On this weekday (0 = Monday ... 6 = Sunday) it uses the Ukrainian-Canadian list below instead.
UKRAINIAN_CANADIAN_DAY = 6

# English Wikipedia article titles, used in order; add your own any time.
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
