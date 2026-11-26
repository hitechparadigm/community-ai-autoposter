"""Where stories come from: news feeds, article pages, photos, Wikipedia."""
import html
import json
import random
import re
import xml.etree.ElementTree as ET
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

from community import config

from .core import ATOM, DC, UA, WIKI, WIKI_UA, http, now


def _txt(el, *names):
    """The text (or href) of the first of these child elements of a feed item that has one."""
    for n in names:
        x = el.find(n)
        if x is not None:
            if x.text and x.text.strip():
                return x.text.strip()
            if x.get("href"):
                return x.get("href").strip()
    return ""


def _date(s):
    """A feed date (RSS or ISO style) as a UTC datetime; None if it can't be read."""
    if not s:
        return None
    try:
        d = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def _clean(s, limit=400):
    """Plain text from an HTML snippet: tags removed, entities decoded, spaces collapsed, cut to limit."""
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()[:limit]


def parse_feed(xml_bytes, source):
    """Stories (source, title, url, summary, published) from an RSS or Atom feed. Links from news-search
    feeds are unwrapped to the real article and credited to the outlet that published it."""
    root = ET.fromstring(xml_bytes)
    entries = root.findall(".//item") or root.findall(f".//{ATOM}entry")
    out = []
    for it in entries:
        title = _clean(_txt(it, "title", f"{ATOM}title"), 200)
        link = _txt(it, "link", f"{ATOM}link").split("#")[0]
        if not title or not link.startswith("http"):
            continue
        outlet = source
        if "bing.com/news/apiclick" in link:  # news search feed: unwrap the real article and credit its outlet
            link = urllib.parse.parse_qs(urllib.parse.urlparse(link).query).get("url", [""])[0]
            if not link.startswith("http"):
                continue
            src = next((e.text for e in it if e.tag.lower().endswith("}source") and e.text), "")
            outlet = (src or outlet_name(link)).strip()
        out.append({
            "source": outlet,
            "title": title,
            "url": link,
            "summary": _clean(_txt(it, "description", f"{ATOM}summary", f"{ATOM}content")),
            "published": _date(_txt(it, "pubDate", f"{ATOM}published", f"{ATOM}updated", f"{DC}date")),
        })
    return out


def fetch_news(seen, max_age_hours=None, limit=220, per_feed=None):
    """Recent items from all feeds that aren't in `seen`, newest first, each tagged with its region.
    per_feed: how many of each feed's newest items to take (default ITEMS_PER_FEED)."""
    per_feed = per_feed or config.ITEMS_PER_FEED
    cutoff = now() - timedelta(hours=max_age_hours or config.MAX_AGE_HOURS)
    items, urls = [], set()
    for name, url, region in config.FEEDS:
        try:
            got = parse_feed(http(url, timeout=45), name)
            print(f"{name}: {len(got)} items")
        except Exception as e:  # one bad feed shouldn't stop the run
            print(f"FEED ERROR {name}: {e}")
            continue
        got.sort(key=lambda i: i["published"] or now(), reverse=True)
        taken = 0
        for it in got:
            community = region not in config.NOT_COMMUNITY_REGIONS and any(
                w in it["title"] + " " + it["summary"] for w in config.COMMUNITY_WORDS)
            if taken >= per_feed and not community:
                continue
            if it["url"] in seen or it["url"] in urls:
                continue
            if it["published"] and it["published"] < cutoff:
                continue
            it["region"] = region
            it["community"] = community or region in config.COMMUNITY_REGIONS
            urls.add(it["url"])
            items.append(it)
            taken += 1
    items.sort(key=lambda i: (i.get("community", False), i["published"] or now()), reverse=True)
    return items[:limit]


BAD_IMG = re.compile(r"logo|icon|favicon|header|banner|avatar|sprite|android-chrome|placeholder|"
                     r"MHS_Archives|social|share|default-image|\.svg|\.gif", re.I)


def _image_size(data):
    """(width, height) from the first bytes of a JPEG or PNG, or None."""
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker, length = data[i + 1], int.from_bytes(data[i + 2:i + 4], "big")
            if marker in (0xC0, 0xC1, 0xC2):
                return int.from_bytes(data[i + 7:i + 9], "big"), int.from_bytes(data[i + 5:i + 7], "big")
            i += 2 + length
    return None


def image_ok(url):
    """A real photo: big enough and not a wide banner or a logo strip."""
    try:
        ua = WIKI_UA if "wikimedia.org" in url else UA
        req = urllib.request.Request(url, headers={"User-Agent": ua, "Range": "bytes=0-131071"})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read(131072)
    except Exception:
        return False
    size = _image_size(data)
    if not size:
        return data[:4] == b"RIFF"  # WebP: can't measure cheaply, accept
    w, h = size
    return w >= 400 and h >= 250 and 0.5 <= w / h <= 2.0


def _find_image(page, url):
    """The page's main picture: og:image or a photo in the content, checked to be a real photo."""
    found = []
    for pat in (r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"',
                r'<meta[^>]+content="([^"]+)"[^>]+property="og:image"',
                r'<img[^>]+src="([^"]+\.(?:jpe?g|png)[^"]*)"'):
        for src in re.findall(pat, page, re.I):
            full = urllib.parse.urljoin(url, html.unescape(src))
            if not BAD_IMG.search(full) and full not in found:
                found.append(full)
    for img in found[:6]:
        if image_ok(img):
            return img
    return ""


def commons_image(query):
    """A freely licensed photo from Wikimedia Commons: the lead image of the English Wikipedia
    article whose title matches the query (so we never grab a picture of something else)."""
    if not query:
        return ""
    if "|" in query:  # several suggestions: the first that finds a photo
        return next((u for q in split_queries(query) if (u := commons_image(q))), "")
    words = set(re.findall(r"\w+", query.lower()))
    for params in ({"titles": query, "redirects": 1},
                   {"generator": "search", "gsrsearch": query, "gsrlimit": 3}):
        q = urllib.parse.urlencode({"action": "query", "prop": "pageimages", "piprop": "original",
                                    "format": "json", **params})
        try:
            pages = json.loads(http(f"{WIKI}/w/api.php?{q}")).get("query", {}).get("pages", {})
        except Exception as e:
            print(f"Commons image search failed: {e}")
            return ""
        for p in sorted(pages.values(), key=lambda p: p.get("index", 0)):
            title = set(re.findall(r"\w+", p.get("title", "").lower()))
            src = (p.get("original") or {}).get("source", "")
            if src and words <= title and not BAD_IMG.search(src) and image_ok(src):
                return src
    # The article has no lead photo: search Wikimedia Commons files whose name shares the key words
    key = {w for w in words if len(w) > 3} or words
    q = urllib.parse.urlencode({"action": "query", "generator": "search", "gsrnamespace": 6, "gsrlimit": 10,
                                "gsrsearch": query, "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 1280,
                                "format": "json"})
    try:
        files = json.loads(http(f"https://commons.wikimedia.org/w/api.php?{q}")).get("query", {}).get("pages", {})
    except Exception as e:
        print(f"Commons file search failed: {e}")
        return ""
    for f in sorted(files.values(), key=lambda p: p.get("index", 99)):
        name = set(re.findall(r"\w+", f.get("title", "").lower()))
        info = (f.get("imageinfo") or [{}])[0]
        src = info.get("thumburl") or info.get("url", "")
        if (len(key & name) >= min(2, len(key)) and re.search(r"\.(jpe?g|png)", src, re.I)
                and not BAD_IMG.search(src) and image_ok(src)):
            return src
    return ""


def fetch_page(url, limit=6000):
    """Best-effort (plain text, main image URL) of an article page."""
    try:
        page = http(url, timeout=30).decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Could not fetch article: {e}")
        return "", ""
    image = _find_image(page, url)
    page = re.sub(r"(?is)<(script|style|noscript|nav|header|footer)[^>]*>.*?</\1>", " ", page)
    for tag in ("article", "main"):  # prefer the main content area when the page marks it
        m = re.search(rf"(?is)<{tag}\b[^>]*>(.*)</{tag}>", page)
        if m and len(m.group(1)) > 2000:
            page = m.group(1)
            break
    paras = [_clean(p, 2000) for p in re.findall(r"(?is)<p[^>]*>(.*?)</p>", page)]
    text = "\n".join(p for p in paras if len(p) > 60)
    return text[:limit], image


def fetch_article(url, limit=6000):
    """The main text of an article page (no image)."""
    return fetch_page(url, limit)[0]


def wiki_thumb(url, width=1280):
    """A smaller copy of a Wikimedia image (originals can be tens of megabytes)."""
    url = url.split("?")[0]
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/(?:commons|en))/(\w/\w\w)/([^/?#]+)$", url)
    if not m or url.lower().endswith(".svg"):
        return url
    return f"{m.group(1)}/thumb/{m.group(2)}/{m.group(3)}/{width}px-{m.group(3)}"


def outlet(source):
    """Media outlet from a feed name, e.g. "CBC Manitoba" -> "CBC" (prefixes in config.OUTLET_PREFIXES)."""
    for name in config.OUTLET_PREFIXES:
        if source.startswith(name):
            return name
    return source


def wiki_text(title, limit=15000):
    """Plain-text article from English Wikipedia: (text, url), empty if missing."""
    q = urllib.parse.urlencode({"action": "query", "prop": "extracts", "explaintext": 1,
                                "redirects": 1, "titles": title, "format": "json"})
    try:
        data = json.loads(http(f"{WIKI}/w/api.php?{q}"))
    except Exception as e:
        print(f"Wikipedia error for {title}: {e}")
        return "", ""
    for page in data.get("query", {}).get("pages", {}).values():
        text = page.get("extract") or ""
        if text:
            real = page.get("title", title)
            url = f"{WIKI}/wiki/" + urllib.parse.quote(real.replace(" ", "_"))
            return text[:limit], url
    return "", ""


def _get_page(url, timeout=40):
    """A page's HTML as text; "" if it can't be loaded."""
    try:
        return http(url, timeout=timeout).decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Could not load {url}: {e}")
        return ""


def harvest(src):
    """Links (url, title) to articles listed on one random index page of a source."""
    tmpl = random.choice(src["index"])
    url = (tmpl.replace("{n}", str(random.randint(src.get("first_page", 1), src.get("pages", 1))))
               .replace("{letter}", random.choice("abcdefghijklmnoprstw"))
               .replace("{LETTER}", random.choice("ABCDEFGHIJKLMNOPRSTW")))
    page = _get_page(url)
    found = {}
    if "<urlset" in page[:2000]:
        pairs = [(u, "") for u in re.findall(r"<loc>([^<]+)</loc>", page)]
    else:
        pairs = re.findall(r'(?is)<a\b[^>]*?href="([^"#]+)"[^>]*>(.*?)</a>', page)
    for href, text in pairs:
        full = urllib.parse.urljoin(url, html.unescape(href))
        if not re.search(src["pattern"], full) or full in found:
            continue
        title = _clean(text, 150)
        if len(title) < 4:
            slug = full.rstrip("/").rsplit("/", 1)[-1]
            title = re.sub(r"\.\w+$|-1\.\d+$", "", slug).replace("-", " ").replace("_", " ")
        found[full] = title
    print(f"{src['name']}: {len(found)} links from {url}")
    return list(found.items())


def people_of_the_day():
    """People born or died on this day, from config.PEOPLE_OF_THE_DAY (a page listing them), or [] if unset."""
    src = getattr(config, "PEOPLE_OF_THE_DAY", None)
    if not src:
        return []
    page = _get_page(src["url"])
    out = {}
    for href, name in re.findall(r'<a\b[^>]*?href="([^"#]+)"[^>]*>(.*?)</a>', page, re.S):
        url = urllib.parse.urljoin(src["url"], html.unescape(href))
        name = _clean(name, 120)
        if re.search(src["pattern"], url) and len(name) > 3 and url not in out:
            out[url] = name
    return [{"url": u, "name": n} for u, n in out.items()]


def best_page(text, pages):
    """The linked page that is about the event itself (e.g. "Canoe River train crash"), not a page about
    something it mentions (e.g. "Canadian National Railway"): most of its title's words appear in the text,
    preferring longer, more specific titles."""
    words = set(re.findall(r"\w+", text.lower()))

    def score(p):
        """How well a Wikipedia page title matches the event's words (share of title words found, title length)."""
        title = re.sub(r"_", " ", p.get("title", ""))
        tw = [w for w in re.findall(r"\w+", title.lower()) if len(w) > 2]
        hit = sum(w in words for w in tw) / len(tw) if tw else 0
        return (hit, len(tw))
    return max(pages, key=score).get("title", "")


def wiki_on_this_day(d):
    """Wikipedia's "On this day" events for a date, each with its year and main article."""
    try:
        data = json.loads(http(f"{WIKI}/api/rest_v1/feed/onthisday/all/{d:%m}/{d:%d}"))
    except Exception as e:
        print(f"On-this-day error: {e}")
        return []
    out = []
    for kind in ("selected", "events", "births", "deaths"):
        for e in data.get(kind, []):
            pages = e.get("pages") or []
            blob = e.get("text", "") + " " + " ".join(p.get("extract", "") for p in pages[:2])
            if pages and any(w in blob for w in config.THISDAY_WORDS):
                out.append({"kind": kind, "year": e.get("year"), "text": e.get("text", ""),
                            "page": best_page(e.get("text", ""), pages)})
    return out


def split_queries(query):
    """'A | B | C' -> ['A', 'B', 'C'] (the writer suggests several picture searches, best first)."""
    return [q.strip() for q in (query or "").split("|") if q.strip()][:4]


def clean_link(url):
    """Remove tracking bits (config.STRIP_FROM_LINKS) from a link."""
    for part in config.STRIP_FROM_LINKS:
        url = url.replace(part, "")
    return url


def page_title(url):
    """A page's title (og:title, or <title>); "" if the page can't be loaded."""
    try:
        page = http(url, timeout=30).decode("utf-8", errors="replace")
    except Exception:
        return ""
    m = (re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', page)
         or re.search(r"(?is)<title[^>]*>(.*?)</title>", page))
    return _clean(html.unescape(m.group(1)), 200) if m else ""


def outlet_name(url):
    """The display name of the feed this link comes from (e.g. Global News), or its domain."""
    host = urllib.parse.urlparse(url).netloc.replace("www.", "")
    for name, feed, _ in config.FEEDS:
        if urllib.parse.urlparse(feed).netloc.replace("www.", "") == host:
            return re.sub(r"\s+(Politics|BC|Calgary|Edmonton|Toronto|Winnipeg|Montreal|Halifax)$", "", name)
    return host


def web_search(query, news=False):
    """Web (or news) search results as feed items (title, url, summary, source), from the search feeds in
    config.RESEARCH; [] if the search fails."""
    tpl = config.RESEARCH["news_search" if news else "web_search"]
    try:
        items = parse_feed(http(tpl.format(q=urllib.parse.quote_plus(query)), timeout=30), "Web")
    except Exception as e:
        print(f"Search failed for '{query}': {str(e)[:100]}")
        return []
    for it in items:
        if it["source"] == "Web":
            it["source"] = outlet_name(it["url"])
    return items
