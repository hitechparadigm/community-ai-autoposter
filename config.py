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

# How many drafts each run sends you for approval (it may send fewer)
DRAFTS_PER_RUN = 2

# Ignore news older than this
MAX_AGE_HOURS = 36

# Drafts not approved within this time are dropped
DRAFT_EXPIRY_HOURS = 24

# Claude model used to pick stories and write posts
MODEL = "claude-sonnet-5-5"
