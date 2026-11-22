import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bot
cbc = ["canada", "politics", "canada-britishcolumbia", "canada-calgary", "canada-edmonton", "canada-saskatchewan",
       "canada-saskatoon", "canada-manitoba", "canada-toronto", "canada-ottawa", "canada-hamiltonnews",
       "canada-kitchenerwaterloo", "canada-london", "canada-windsor", "canada-sudbury", "canada-thunderbay",
       "canada-montreal", "canada-newbrunswick", "canada-novascotia", "canada-pei", "canada-newfoundland",
       "canada-north", "indigenous"]
gn = ["canada", "politics", "bc", "calgary", "edmonton", "lethbridge", "regina", "saskatoon", "winnipeg", "toronto",
      "ottawa", "kingston", "montreal", "halifax", "new-brunswick", "peterborough", "london", "guelph"]
urls = [f"https://www.cbc.ca/webfeed/rss/rss-{x}" for x in cbc] + [f"https://globalnews.ca/{x}/feed/" for x in gn]
for u in urls:
    try:
        items = bot.parse_feed(bot.http(u, timeout=45), "x")
        newest = max((i["published"] for i in items if i["published"]), default=None)
        print(f"### OK {len(items):3d} newest {newest:%m-%d %H:%M} {u}" if newest else f"### OK {len(items):3d} {u}")
    except Exception as e:
        print(f"### FAIL {u}: {str(e)[:80]}")
