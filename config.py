# Settings for the Ukrainian Canada autoposter. Edit freely.

# Telegram channel where approved posts go
CHANNEL = "@UkrainianCanada"

# News sources: (display name, RSS/Atom feed URL, region)
# If a feed stops working, the run log shows "FEED ERROR" and the rest still run.
# National Post isn't here: its feeds don't return a readable feed to automated requests.
# Its sister Postmedia papers below (Vancouver Sun, Calgary Herald, ...) work.
FEEDS = [
    # National
    ("CBC News", "https://www.cbc.ca/webfeed/rss/rss-canada", "Canada"),
    ("CBC Politics", "https://www.cbc.ca/webfeed/rss/rss-politics", "Canada"),
    ("Global News", "https://globalnews.ca/canada/feed/", "Canada"),
    ("Global News Politics", "https://globalnews.ca/politics/feed/", "Canada"),
    # British Columbia
    ("CBC British Columbia", "https://www.cbc.ca/webfeed/rss/rss-canada-britishcolumbia", "British Columbia"),
    ("Global News BC", "https://globalnews.ca/bc/feed/", "British Columbia"),
    ("Vancouver Sun", "https://vancouversun.com/feed/", "British Columbia"),
    # Alberta
    ("CBC Calgary", "https://www.cbc.ca/webfeed/rss/rss-canada-calgary", "Alberta"),
    ("CBC Edmonton", "https://www.cbc.ca/webfeed/rss/rss-canada-edmonton", "Alberta"),
    ("Global News Calgary", "https://globalnews.ca/calgary/feed/", "Alberta"),
    ("Global News Edmonton", "https://globalnews.ca/edmonton/feed/", "Alberta"),
    ("Calgary Herald", "https://calgaryherald.com/feed/", "Alberta"),
    ("Edmonton Journal", "https://edmontonjournal.com/feed/", "Alberta"),
    # Saskatchewan
    ("CBC Saskatchewan", "https://www.cbc.ca/webfeed/rss/rss-canada-saskatchewan", "Saskatchewan"),
    ("Global News Regina", "https://globalnews.ca/regina/feed/", "Saskatchewan"),
    ("Global News Saskatoon", "https://globalnews.ca/saskatoon/feed/", "Saskatchewan"),
    # Manitoba
    ("CBC Manitoba", "https://www.cbc.ca/webfeed/rss/rss-canada-manitoba", "Manitoba"),
    ("Global News Winnipeg", "https://globalnews.ca/winnipeg/feed/", "Manitoba"),
    # Ontario
    ("CBC Toronto", "https://www.cbc.ca/webfeed/rss/rss-canada-toronto", "Ontario"),
    ("CBC Ottawa", "https://www.cbc.ca/webfeed/rss/rss-canada-ottawa", "Ontario"),
    ("Global News Toronto", "https://globalnews.ca/toronto/feed/", "Ontario"),
    ("Global News Ottawa", "https://globalnews.ca/ottawa/feed/", "Ontario"),
    ("Ottawa Citizen", "https://ottawacitizen.com/feed/", "Ontario"),
    ("Toronto Sun", "https://torontosun.com/feed/", "Ontario"),
    # Quebec
    ("CBC Montreal", "https://www.cbc.ca/webfeed/rss/rss-canada-montreal", "Quebec"),
    ("Global News Montreal", "https://globalnews.ca/montreal/feed/", "Quebec"),
    # Atlantic
    ("CBC New Brunswick", "https://www.cbc.ca/webfeed/rss/rss-canada-newbrunswick", "New Brunswick"),
    ("Global News New Brunswick", "https://globalnews.ca/new-brunswick/feed/", "New Brunswick"),
    ("CBC Nova Scotia", "https://www.cbc.ca/webfeed/rss/rss-canada-novascotia", "Nova Scotia"),
    ("Global News Halifax", "https://globalnews.ca/halifax/feed/", "Nova Scotia"),
    ("CBC PEI", "https://www.cbc.ca/webfeed/rss/rss-canada-pei", "Prince Edward Island"),
    ("CBC Newfoundland and Labrador", "https://www.cbc.ca/webfeed/rss/rss-canada-newfoundland", "Newfoundland and Labrador"),
    # Yukon, Northwest Territories, Nunavut
    ("CBC North", "https://www.cbc.ca/webfeed/rss/rss-canada-north", "Territories (Yukon, NWT, Nunavut)"),
    # Ukrainian community in Canada
    ("New Pathway", "https://newpathway.ca/feed/", "Ukrainian community in Canada"),
    ("UCC Manitoba", "https://www.uccmanitoba.ca/feed/", "Ukrainian community in Canada"),
    # Ukraine
    ("Ukrinform", "https://www.ukrinform.net/rss/block-lastnews", "Ukraine"),
]

# Newest items taken from each feed per run (keeps big feeds from crowding out small ones).
# Stories about the Ukrainian community are always kept, whatever their position in the feed.
ITEMS_PER_FEED = 8
COMMUNITY_WORDS = ("Ukrain", "україн", "Україн")

# Drafts each run sends you (it may send fewer). 5 runs a day x 1 = up to 5 posts/day.
# Set to 2 to get a backup option each run.
DRAFTS_PER_RUN = 1

# Ignore news older than this
MAX_AGE_HOURS = 36

# Drafts not approved within this time are dropped
DRAFT_EXPIRY_HOURS = 24

# Daily digest (python bot.py digest): top national news plus 3-4 provinces/territories, rotating
DIGEST_NATIONAL = "3-5"
DIGEST_REGIONS = "3-4"

# Referral links: one per morning digest, in rotation: (text, link, what it is).
# Update the amounts here when an offer changes.
REFERRALS = [
    ("📈 Почніть інвестувати з Wealthsimple і отримайте $25", "https://www.wealthsimple.com/invite/L4FYWG",
     "Wealthsimple investing and savings account"),
    ("💳 Дізнайтеся свій кредитний рейтинг безкоштовно", "https://bit.ly/my-credit-score",
     "free credit score check"),
    ("🏦 Відкрийте рахунок у Simplii і отримайте $50", "https://blue.mbsy.co/6svHvM",
     "Simplii Financial no-fee bank account"),
    ("💸 Перший переказ в Україну з Wise — без комісії", "https://bit.ly/3UYzy9r",
     "Wise international money transfers (e.g. to Ukraine)"),
    ("📊 Інвестуйте з Questrade і отримайте $50", "https://bit.ly/4dUdlWV", "Questrade investing account"),
    ("💳 Перевірте свій кредитний рейтинг", "https://bit.ly/3cqN99x", "free credit score check"),
]
REFERRAL_DISCLOSURE = ""  # optional line under the link, e.g. "#реклама"; empty = none

# Claude model used to pick, write and copy-edit posts (Sonnet 5.5)
MODEL = "claude-sonnet-5-5"

# ---------- Canadian history ----------
# History posts are long-reads on Telegraph (telegra.ph, opens inside Telegram); the channel gets a teaser.
TELEGRAPH_AUTHOR = "Українська Канада"
TELEGRAPH_AUTHOR_URL = "https://t.me/UkrainianCanada"

# Canadian sources come first; Wikipedia is used only when they give nothing usable.
# "📅 Цей день в історії Канади" (daily): a person born or died on today's date, from the
#   Dictionary of Canadian Biography (fallback: Wikipedia "On this day", Canadian entries).
# "🍁 Історія Канади" (daily): a story picked from HISTORY_SOURCES (fallback: WIKI_REGIONAL_TOPICS).
# On this weekday (0 = Monday ... 6 = Sunday) it tells a Ukrainian-Canadian story instead,
#   from UKRAINIAN_CANADIAN_SOURCES (fallback: UKRAINIAN_CANADIAN_TOPICS on Wikipedia).
UKRAINIAN_CANADIAN_DAY = 6

# Ukrainian-Canadian stories from Canadian archives and heritage sites (their own search pages).
UKRAINIAN_CANADIAN_SOURCES = [
    {"name": "Library and Archives Canada", "region": "Ukrainian Canadians",
     "index": ["https://thediscoverblog.com/?s=ukrainian", "https://thediscoverblog.com/page/2/?s=ukrainian",
               "https://thediscoverblog.com/?s=internment"],
     "pattern": r"thediscoverblog\.com/\d{4}/\d{2}/\d{2}/[a-z0-9-]+/$"},
    {"name": "RETROactive: Alberta's Historic Places", "region": "Ukrainian Canadians",
     "index": ["https://albertashistoricplaces.com/?s=ukrainian", "https://albertashistoricplaces.com/page/2/?s=ukrainian"],
     "pattern": r"albertashistoricplaces\.com/\d{4}/\d{2}/\d{2}/[a-z0-9-]+/$"},
    {"name": "Canadian First World War Internment Recognition Fund", "region": "Ukrainian Canadians",
     "index": ["https://www.internmentcanada.ca/"],
     "pattern": r"internmentcanada\.ca/[a-z0-9-]+/?$"},
]

# Wikipedia fallback for Ukrainian-Canadian Sundays (English article titles, used in order).
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
     "pages": 15, "pattern": r"albertashistoricplaces\.com/\d{4}/\d{2}/\d{2}/[a-z0-9-]+/$"},
]

# Words that mark a Wikipedia "On this day" entry as Canadian
CANADA_WORDS = ("Canad", "Quebec", "Québec", "Ontario", "Manitoba", "Saskatchewan", "Alberta",
                "British Columbia", "Nova Scotia", "New Brunswick", "Newfoundland", "Labrador",
                "Prince Edward Island", "Yukon", "Nunavut", "Northwest Territories", "Toronto",
                "Montreal", "Montréal", "Vancouver", "Winnipeg", "Ottawa", "Halifax", "Calgary",
                "Edmonton", "Regina", "Saskatoon", "Hudson's Bay", "Klondike", "Mountie")

# Wikipedia fallback when the sources above give nothing usable, and the main coverage for regions
# whose history sites can't be read automatically (they block bots or need JavaScript):
# BC, the Atlantic provinces and the North. Add your own: ("Region", "Article title").
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
