import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bot
for u in ["https://www.ucc.ca/feed/", "https://newpathway.ca/feed/", "https://ukrainianews.com/feed/",
          "https://www.ukrainianweekly.com/feed/", "https://www.uccmanitoba.ca/feed/", "https://uccmanitoba.ca/feed/",
          "https://www.kontakt.ca/feed/", "https://ucrdc.org/feed/"]:
    try:
        items = bot.parse_feed(bot.http(u, timeout=45), "x")
        newest = max((i["published"] for i in items if i["published"]), default=None)
        print(f"### OK {len(items):3d} newest {newest} {u} | {items[0]['title'][:70] if items else ''}")
    except Exception as e:
        print(f"### FAIL {u}: {str(e)[:90]}")
