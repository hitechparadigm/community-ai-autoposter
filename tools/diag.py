import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bot
for u in ["https://nationalpost.com/feed/", "https://nationalpost.com/category/news/canada/feed/",
          "https://nationalpost.com/category/news/politics/feed/",
          "https://vancouversun.com/feed/", "https://calgaryherald.com/feed/", "https://edmontonjournal.com/feed/",
          "https://leaderpost.com/feed/", "https://thestarphoenix.com/feed/", "https://winnipegsun.com/feed/",
          "https://ottawacitizen.com/feed/", "https://montrealgazette.com/feed/", "https://torontosun.com/feed/"]:
    try:
        items = bot.parse_feed(bot.http(u, timeout=45), "x")
        newest = max((i["published"] for i in items if i["published"]), default=None)
        print(f"### OK {len(items):3d} newest {newest} {u} | {items[0]['title'][:60] if items else ''} | summary {len(items[0]['summary']) if items else 0}")
    except Exception as e:
        print(f"### FAIL {u}: {str(e)[:80]}")
