import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bot
from urllib.parse import urljoin
def get(u):
    try: return bot.http(u, timeout=40).decode("utf-8", "replace")
    except Exception as e: return "ERR " + str(e)[:80]
S = [
 ("CBC Archives", "https://www.cbc.ca/archives/history", r'/archives/[a-z0-9-]+-1\.\d+'),
 ("MHS people K", "https://www.mhs.mb.ca/docs/people/index_k.shtml", r'/docs/people/[a-z][a-z0-9_]*_[a-z0-9_]+\.shtml'),
 ("MHS sites buildings", "https://www.mhs.mb.ca/docs/sites/index_buildings.shtml", r'/docs/sites/(?!index)[a-z0-9_]+\.shtml'),
 ("eSask B", "https://esask.uregina.ca/entry_list-l=B.html", r'entry/[a-z0-9_]+\.html'),
 ("RETROactive", "https://albertashistoricplaces.com/category/subject/albertas-history-subject/page/3/", r'https://albertashistoricplaces\.com/\d{4}/\d{2}/\d{2}/[a-z0-9-]+/'),
 ("QAHN", "https://qahn.org/article?page=3", r'/article/[a-z0-9-]+'),
 ("LAC blog p5", "https://thediscoverblog.com/page/5/", r'https://thediscoverblog\.com/\d{4}/\d{2}/\d{2}/[a-z0-9-]+/'),
 ("OHT articles", "https://www.heritagetrust.on.ca/sitemaps-1-section-articles-1-sitemap.xml", r'<loc>([^<]+)</loc>'),
 ("OHT bios", "https://www.heritagetrust.on.ca/sitemaps-1-section-biographyItems-1-sitemap.xml", r'<loc>([^<]+)</loc>'),
 ("DCB new", "http://www.biographi.ca/en/new_biographies.html", r'href="([^"]*bio[^"#]*\.html)"'),
 ("Pier21 search", "https://pier21.ca/search?page=31", r'href="(/research/[^"]+/[^"]+)"'),
 ("Pier21 immig hist p1", "https://pier21.ca/research/immigration-history?page=1", r'href="(/[^"]*immigration-history/[^"]+)"'),
 ("PWNHC exhibits", "https://www.pwnhc.ca/en/exhibits/past", r'href="(/en/exhibits/[a-z0-9-]+)"'),
 ("Royal BC Museum", "https://royalbcmuseum.bc.ca/", r'href="([^"]*(?:blog|stories|learn)[^"]*)"'),
 ("NB Museum", "https://www.nbm-mnb.ca/", r'href="([^"]+)"'),
 ("NS Museum", "https://museum.novascotia.ca/", r'href="([^"]+)"'),
 ("Vancouver History", "https://www.vancouverheritagefoundation.org/", r'href="([^"]*(?:stor|blog|histor)[^"]*)"'),
]
for name, url, pat in S:
    html = get(url)
    links = []
    for l in re.findall(pat, html):
        l = urljoin(url, l)
        if l not in links: links.append(l)
    print(f"\n### {name} | {'ERR' if html.startswith('ERR') else len(html)} | {len(links)} links  {html[:80] if html.startswith('ERR') else ''}")
    for l in links[:5]: print("    ", l[:130])
    pick = next((l for l in links[3:] + links[:3] if not l.endswith('.xml')), None)
    if pick:
        txt = bot.fetch_article(pick)
        print(f"    ARTICLE {pick[:90]} -> {len(txt)} chars: {txt[:160]!r}")
