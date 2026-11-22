"""Temporary: check which history sources can be read from GitHub and what their links look like."""
import re, sys, urllib.request
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=40) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except Exception as e:
        return str(e)[:80], ""
C = [
 ("TCE browse", "https://www.thecanadianencyclopedia.ca/en/browse/things/history?page=3", r'/en/article/[a-z0-9-]+'),
 ("TCE timelines", "https://www.thecanadianencyclopedia.ca/en/timelines", r'/en/timeline/[a-z0-9-]+'),
 ("TCE timelines places", "https://www.thecanadianencyclopedia.ca/en/timelines/places", r'/en/timeline/[a-z0-9-]+'),
 ("TCE yukon", "https://www.thecanadianencyclopedia.ca/en/timeline/yukon", r'/en/article/[a-z0-9-]+'),
 ("Canada's History", "https://www.canadashistory.ca/explore/all-stories", r'/explore/[a-z0-9-]+/[a-z0-9-]+'),
 ("Canada's History p2", "https://www.canadashistory.ca/explore/all-stories?page=2", r'/explore/[a-z0-9-]+/[a-z0-9-]+'),
 ("CBC Archives", "https://www.cbc.ca/archives/history", r'/archives/[a-z0-9-]+-1\.\d+'),
 ("CBC Archives home", "https://www.cbc.ca/archives", r'/archives/[a-z0-9-]+-1\.\d+'),
 ("DCB", "http://www.biographi.ca/en/", r'/en/bio/[a-z0-9_]+\.html'),
 ("Pier 21", "https://pier21.ca/research/immigration-history", r'/research/immigration-history/[a-z0-9-]+'),
 ("MHS people", "https://www.mhs.mb.ca/docs/people/index_k.shtml", r'/docs/people/[a-z0-9_]+\.shtml'),
 ("MHS sites", "https://www.mhs.mb.ca/docs/sites/index.shtml", r'/docs/sites/[a-z0-9_]+\.shtml'),
 ("eSask", "https://esask.uregina.ca/entry_list-l=B.html", r'entry/[a-z0-9_]+\.html'),
 ("RETROactive", "https://albertashistoricplaces.com/category/subject/albertas-history-subject/page/3/", r'albertashistoricplaces\.com/\d{4}/\d{2}/\d{2}/[a-z0-9-]+/'),
 ("NL Heritage", "https://www.heritage.nf.ca/toc/site-map.php", r'/articles/[a-z0-9-]+/[a-z0-9-]+\.php'),
 ("QAHN", "https://qahn.org/article?page=3", r'/article/[a-z0-9-]+'),
 ("TPL Ontario", "https://blogs.tpl.ca/digital-archive-ontario/2018/12/list-of-all-blog-posts/", r'blogs\.tpl\.ca/[a-z0-9-]+/\d{4}/\d{2}/[a-z0-9-]+/'),
 ("BCHF", "https://www.bchistory.ca/", r'href="([^"]+)"'),
 ("ActiveHistory feed", "https://activehistory.ca/feed/", r'<link>[^<]+</link>'),
 ("LAC blog feed", "https://thediscoverblog.com/feed/", r'<link>[^<]+</link>'),
]
for name, url, pat in C:
    st, html = get(url)
    links = sorted(set(re.findall(pat, html)))
    print(f"\n### {name} | {st} | {len(html)} bytes | {len(links)} links")
    for l in links[:6]:
        print("   ", l[:120])
# raw structure of a TCE timeline entry
st, html = get("https://www.thecanadianencyclopedia.ca/en/timeline/manitoba")
i = html.find("1869")
print("\n### TCE timeline raw around first date:\n", re.sub(r"\s+", " ", html[max(0, i-1500):i+1200]))
