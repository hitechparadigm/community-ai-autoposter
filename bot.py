#!/usr/bin/env python3
"""Ukrainian Canada autoposter.

  python bot.py draft    - fetch news, have Claude pick and write posts (Ukrainian),
                           send drafts to you in Telegram with Publish / Skip buttons
  python bot.py thisday  - draft one "This day in Canadian history" post
  python bot.py history  - draft one "Canadian history" story
  python bot.py approve  - check your button taps and publish approved posts to the channel

No third-party packages needed (standard library only).
"""
import hashlib
import html
import json
import os
import random
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

import config

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(HERE, "state.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")
ATOM = "{http://www.w3.org/2005/Atom}"
DC = "{http://purl.org/dc/elements/1.1/}"

TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
# One or more approver IDs, comma-separated (e.g. "456360947,123456789")
ADMIN_IDS = [x.strip() for x in os.environ.get("TELEGRAM_ADMIN_ID", "").split(",") if x.strip()]
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")


# ---------- helpers ----------

def now():
    return datetime.now(timezone.utc)


def http(url, data=None, headers=None, timeout=30):
    h = {"User-Agent": UA}
    h.update(headers or {})
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        raise RuntimeError(f"HTTP {e.code} from {url.split('?')[0]}: {detail}") from None


def load_state():
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            s = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        s = {}
    s.setdefault("seen", {})      # url -> ISO time first seen
    s.setdefault("pending", {})   # draft id -> draft
    s.setdefault("tg_offset", 0)
    return s


def save_state(s):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=1, sort_keys=True)


def merge_state(base, ours, theirs):
    """Three-way merge when two runs saved state at the same time.
    theirs = state already on GitHub, ours = this run's state, base = what this run started from."""
    out = json.loads(json.dumps(theirs))
    for k in ("seen", "pending"):
        out.setdefault(k, {})
    for did, d in ours.get("pending", {}).items():
        if did not in base.get("pending", {}):
            out["pending"][did] = d            # we added a draft
    for did in base.get("pending", {}):
        if did not in ours.get("pending", {}):
            out["pending"].pop(did, None)      # we published, skipped or expired it
    out["seen"].update(ours.get("seen", {}))
    done = out.get("history_done", [])
    out["history_done"] = done + [x for x in ours.get("history_done", []) if x not in done]
    out["tg_offset"] = max(theirs.get("tg_offset", 0), ours.get("tg_offset", 0))
    return out


def tg(method, **params):
    if not TG_TOKEN:
        sys.exit("TELEGRAM_BOT_TOKEN is not set")
    raw = http(f"https://api.telegram.org/bot{TG_TOKEN}/{method}", params)
    resp = json.loads(raw)
    if not resp.get("ok"):
        raise RuntimeError(f"Telegram {method} failed: {resp}")
    return resp["result"]


# ---------- feeds ----------

def _txt(el, *names):
    for n in names:
        x = el.find(n)
        if x is not None:
            if x.text and x.text.strip():
                return x.text.strip()
            if x.get("href"):
                return x.get("href").strip()
    return ""


def _date(s):
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
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()[:limit]


def parse_feed(xml_bytes, source):
    root = ET.fromstring(xml_bytes)
    entries = root.findall(".//item") or root.findall(f".//{ATOM}entry")
    out = []
    for it in entries:
        title = _clean(_txt(it, "title", f"{ATOM}title"), 200)
        link = _txt(it, "link", f"{ATOM}link").split("#")[0]
        if not title or not link.startswith("http"):
            continue
        out.append({
            "source": source,
            "title": title,
            "url": link,
            "summary": _clean(_txt(it, "description", f"{ATOM}summary", f"{ATOM}content")),
            "published": _date(_txt(it, "pubDate", f"{ATOM}published", f"{ATOM}updated", f"{DC}date")),
        })
    return out


def fetch_news(seen):
    cutoff = now() - timedelta(hours=config.MAX_AGE_HOURS)
    items, urls = [], set()
    for name, url in config.FEEDS:
        try:
            got = parse_feed(http(url, timeout=45), name)
            print(f"{name}: {len(got)} items")
        except Exception as e:  # one bad feed shouldn't stop the run
            print(f"FEED ERROR {name}: {e}")
            continue
        for it in got:
            if it["url"] in seen or it["url"] in urls:
                continue
            if it["published"] and it["published"] < cutoff:
                continue
            urls.add(it["url"])
            items.append(it)
    items.sort(key=lambda i: i["published"] or now(), reverse=True)
    return items[:60]


# ---------- Claude ----------

AUDIENCE = """You are the editor of "Ukrainian Canada", a Telegram channel for Ukrainians living in Canada \
(recent arrivals including CUAET, and the long-established community). The channel covers immigration, \
adaptation and life in Canada."""

PICK_PROMPT = AUDIENCE + """

Below are fresh news items. Pick up to {n} that matter most to this audience, for example: immigration, \
status and permits, CUAET, government programs and benefits, cost of living, housing, jobs, \
Canada-Ukraine relations, Canadian support for Ukraine, Ukrainian community life in Canada, \
or major national news everyone in Canada is talking about. Skip routine crime, celebrity and sports stories. \
Never pick two items about the same story. Pick fewer, or none, if nothing is relevant.

Reply with JSON only: a list of the chosen item ids, most important first, e.g. [4, 17]

News items:
{items}
"""

STYLE = """Language standard: literary Ukrainian at the level of a professional news editor \
(Суспільне, Українська правда, Радіо Свобода).
- Write natural Ukrainian, not a translation from English. Rebuild English sentence structure; avoid calques \
and bureaucratic wording.
- No russianisms or surzhyk. Examples of errors: "приймати участь" (correct: брати участь), "на протязі" \
(протягом), "являється" (є), "слідуючий" (наступний), "в якості" (як), "співпадати" (збігатися), \
"міроприємство" (захід), "згідно закону" (згідно із законом), "вірно" in the sense of correct (правильно).
- Check every word's meaning: "прибульці" means aliens from space; newcomers are "новоприбулі", \
"новоприбулі українці", "ті, хто нещодавно приїхав".
- Canadian terms: IRCC = Міністерство імміграції, біженців і громадянства Канади (IRCC); permanent residence = \
постійне резидентство (PR); work permit = дозвіл на роботу; study permit = дозвіл на навчання; \
provincial premier = прем'єр провінції (e.g. прем'єр Онтаріо); Prime Minister = прем'єр-міністр Канади; \
Parliament / House of Commons = парламент / Палата громад; amounts: "50 млн доларів".
- People: on first mention give the Ukrainian transliteration, the original English spelling in brackets, \
and their role (e.g. міністерка промисловості Канади Мелані Жолі (Mélanie Joly); Фостер Г'юїтт (Foster Hewitt)). \
Later mentions: Ukrainian only. Do the same for lesser-known places, venues and organizations \
(e.g. «Мейпл-Ліф-Гарденс» (Maple Leaf Gardens)); well-known names like Торонто or Оттава need no brackets. \
Use feminine job titles for women.
- Typography: apostrophe ' (м'ясо), em dash with spaces " — ", quotation marks «...», no double spaces.
- Prefer short sentences and active voice. No clichés, no filler, no exclamation marks, no clickbait."""

WRITE_PROMPT = AUDIENCE + "\n\n" + STYLE + """

Write a Telegram post in Ukrainian about the news article below. Readers should understand the story \
without opening the link.

- "title": a short headline, at most 12 words
- "body": 2-3 short paragraphs (about 600-1000 characters in total), separated by blank lines:
  1. What happened, in plain words.
  2. The key details: who, numbers, dates, deadlines, who is eligible or affected.
  3. Why it matters for Ukrainians in Canada, and what they can do next if anything (only if it really applies).
- Write in your own words; never copy sentences from the article.
- Use only facts stated in the article; do not invent or guess details. If the article text is missing, \
keep the post shorter and stick to the headline and summary.
- Neutral, clear, friendly tone. No hashtags, no emojis in the body.

Reply with JSON only: {{"title": "...", "body": "..."}}

Source: {source}
Headline: {title}
Summary: {summary}
Article text:
{article}
"""

EDIT_PROMPT = """You are the copy editor of a Ukrainian news channel. Edit this draft post to publication quality.

""" + STYLE + """

Check and fix:
1. Spelling, grammar, punctuation, typography.
2. Russianisms, surzhyk, calques from English, unnatural or awkward phrasing, wrong word choice.
3. Facts: every name, number, date and claim must match the article. Remove anything the article does not support.
4. Clarity: a reader who has not seen the article must understand it. Keep the structure and length.

If the draft is already correct, return it unchanged. Reply with JSON only: {{"title": "...", "body": "..."}}

Draft:
{draft}

Article (for fact-checking):
Headline: {title}
Summary: {summary}
{article}
"""


def ask_claude(prompt):
    if not ANTHROPIC_KEY:
        sys.exit("ANTHROPIC_API_KEY is not set")
    raw = http(
        "https://api.anthropic.com/v1/messages",
        {"model": config.MODEL, "max_tokens": 4000,
         "messages": [{"role": "user", "content": prompt}]},
        {"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01"},
        timeout=180,
    )
    resp = json.loads(raw)
    return "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")


def _json(text, open_ch, close_ch):
    start, end = text.find(open_ch), text.rfind(close_ch)
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start:end + 1], strict=False)
    except json.JSONDecodeError:
        return None


def parse_picks(text):
    ids = _json(text, "[", "]") or []
    return [int(i) for i in ids if isinstance(i, (int, str)) and str(i).isdigit()]


def parse_post(text):
    post = _json(text, "{", "}")
    if isinstance(post, dict) and post.get("title") and post.get("body"):
        return post
    return None


BAD_IMG = re.compile(r"logo|icon|favicon|header|banner|avatar|sprite|android-chrome|placeholder|\.svg|\.gif", re.I)


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
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Range": "bytes=0-131071"})
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
    """A freely licensed photo from Wikimedia Commons, via the best-matching English Wikipedia article."""
    if not query:
        return ""
    q = urllib.parse.urlencode({"action": "query", "generator": "search", "gsrsearch": query, "gsrlimit": 3,
                                "prop": "pageimages", "piprop": "original", "format": "json"})
    try:
        pages = json.loads(http(f"https://en.wikipedia.org/w/api.php?{q}")).get("query", {}).get("pages", {})
    except Exception as e:
        print(f"Commons image search failed: {e}")
        return ""
    for p in sorted(pages.values(), key=lambda p: p.get("index", 99)):
        src = (p.get("original") or {}).get("source", "")
        if src and not BAD_IMG.search(src) and image_ok(src):
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
    return fetch_page(url, limit)[0]


# ---------- posts ----------

def format_post(title, body, source, url, header=""):
    e = html.escape
    top = f"{e(header, quote=False)}\n\n" if header else ""
    return (f"{top}<b>{e(title, quote=False)}</b>\n\n{e(body, quote=False)}\n\n"
            f"🔗 Джерело: <a href=\"{e(url, quote=True)}\">{e(source)}</a>")


def buttons(did):
    return {"inline_keyboard": [[
        {"text": "✅ Publish", "callback_data": f"pub:{did}"},
        {"text": "❌ Skip", "callback_data": f"skip:{did}"},
    ]]}


def preview(url):
    return {"url": url, "prefer_large_media": True}


def close_draft(d, status):
    """On every approver's copy of the draft, replace the buttons with a status line."""
    msgs = d.get("msgs") or [[ADMIN_IDS[0], d["admin_msg_id"]]]  # older drafts stored one id
    for chat_id, msg_id in msgs:
        try:
            tg("editMessageText", chat_id=chat_id, message_id=msg_id,
               text=d["text"] + f"\n\n— {status}", parse_mode="HTML",
               link_preview_options={"is_disabled": True})
        except Exception as e:
            print(f"Could not update draft message for {chat_id}: {e}")


# ---------- commands ----------

def cmd_draft():
    if not ADMIN_IDS:
        sys.exit("TELEGRAM_ADMIN_ID is not set")
    s = load_state()
    week_ago = (now() - timedelta(days=7)).isoformat()
    s["seen"] = {u: t for u, t in s["seen"].items() if t > week_ago}

    items = fetch_news(s["seen"])
    print(f"{len(items)} new items")
    if not items:
        save_state(s)
        return

    listing = "\n".join(
        f"[{i}] ({it['source']}) {it['title']} — {it['summary']}" for i, it in enumerate(items))
    picks = parse_picks(ask_claude(PICK_PROMPT.format(n=config.DRAFTS_PER_RUN, items=listing)))
    print(f"Claude picked {picks}")

    stamp = now().isoformat()
    for it in items:  # don't offer the same stories again next run
        s["seen"][it["url"]] = stamp

    for i in picks[:config.DRAFTS_PER_RUN]:
        if i >= len(items):
            continue
        it = items[i]
        article = fetch_article(it["url"])
        post = parse_post(ask_claude(WRITE_PROMPT.format(
            source=it["source"], title=it["title"], summary=it["summary"],
            article=article or "(not available)")))
        if not post:
            print(f"Could not write post for: {it['title']}")
            continue
        edited = parse_post(ask_claude(EDIT_PROMPT.format(
            draft=json.dumps(post, ensure_ascii=False), title=it["title"],
            summary=it["summary"], article=article or "(not available)")))
        if edited:
            post = edited
        else:
            print("Copy edit failed; using the first draft")
        text = format_post(post["title"], post["body"], it["source"], it["url"])
        if not send_draft(s, it["url"], text, stamp):
            continue
        print(f"Draft sent: {it['title']}")
    save_state(s)


def send_draft(s, url, text, stamp, image=""):
    """Send a draft with Publish/Skip buttons to every approver and remember it.
    With an image, the picture is shown above the post (via an invisible link) instead of the source preview."""
    did = hashlib.sha1(url.encode()).hexdigest()[:10]
    if image:
        text = f'<a href="{html.escape(image, quote=True)}">&#8203;</a>' + text
        lp = {"url": image, "prefer_large_media": True, "show_above_text": True}
    else:
        lp = preview(url)
    msgs = []
    for admin in ADMIN_IDS:
        try:
            msg = tg("sendMessage", chat_id=admin, text=text, parse_mode="HTML",
                     link_preview_options=lp, reply_markup=buttons(did))
            msgs.append([admin, msg["message_id"]])
        except Exception as e:  # e.g. this approver never pressed Start in the bot
            print(f"Could not send draft to {admin}: {e}")
    if msgs:
        s["pending"][did] = {"url": url, "text": text, "created": stamp, "msgs": msgs, "lp": lp}
    return bool(msgs)


# ---------- Canadian history ----------
# Two daily columns, both approved like the news:
#   "📅 Цей день в історії Канади" (python bot.py thisday) - an event, birth or death on today's date
#   "🍁 Історія Канади"            (python bot.py history) - a story from the history sources in config.py

CANADA_WORDS = ("Canad", "Quebec", "Québec", "Ontario", "Manitoba", "Saskatchewan", "Alberta",
                "British Columbia", "Nova Scotia", "New Brunswick", "Newfoundland", "Labrador",
                "Prince Edward Island", "Yukon", "Nunavut", "Northwest Territories", "Toronto",
                "Montreal", "Montréal", "Vancouver", "Winnipeg", "Ottawa", "Halifax", "Calgary",
                "Edmonton", "Regina", "Saskatoon", "Hudson's Bay", "Klondike", "Mountie")

THISDAY_PICK_PROMPT = AUDIENCE + """

For the daily "This day in Canadian history" post, pick the ONE most interesting entry below. \
Prefer events and people that teach readers something important or surprising about Canada: \
nation-building moments, firsts, discoveries, remarkable people, immigration and community history. \
Avoid trivia, dry administrative events and anything gruesome.

Reply with JSON only: [<entry id>] (or [] if none is worth a post)

Entries:
{items}
"""

STORY_PICK_PROMPT = AUDIENCE + """

For the daily "Canadian history" column, rank the 3 most promising articles below. \
Goal: educate newcomers about Canada's history across all provinces and territories, with stories \
that are interesting to read: remarkable people, turning points, how places and communities began, \
immigration, daily life in the past. Skip routine notices, events listings, obituaries of minor figures \
and anything without a real story.

Reply with JSON only: a list of up to 3 ids, best first, e.g. [7, 2, 11]

Articles:
{items}
"""

HISTORY_WRITE_PROMPT = AUDIENCE + "\n\n" + STYLE + """

Write a Canadian history post in Ukrainian based on the source text below. \
It should read like a good magazine column: engaging, educational and strictly accurate.

- "title": a short, intriguing headline, at most 12 words (no clickbait, no exclamation marks)
- "body": 3-4 short paragraphs (about 900-1400 characters in total), separated by blank lines. \
{opening} Then tell the story, then explain why it matters or what it left behind. \
Give enough context (where, when, who) for a newcomer who does not know Canadian history. \
Mention a connection to Ukrainians in Canada only if the source supports it.
- Write in your own words. Use only facts stated in the source; do not invent dialogue, details, dates or numbers.

- "image_query": the main person, place or event in English, as it would be titled on English Wikipedia \
(e.g. "Maude Abbott"), used to find a photo.

Reply with JSON only: {{"title": "...", "body": "...", "image_query": "..."}}

Topic: {topic}
Source: {source}
Text:
{article}
"""

LOCAL = timezone(timedelta(hours=-5))  # Toronto (standard time is close enough for picking a date)


def wiki_text(title, limit=7000):
    """Plain-text article from English Wikipedia: (text, url), empty if missing."""
    q = urllib.parse.urlencode({"action": "query", "prop": "extracts", "explaintext": 1,
                                "redirects": 1, "titles": title, "format": "json"})
    try:
        data = json.loads(http(f"https://en.wikipedia.org/w/api.php?{q}"))
    except Exception as e:
        print(f"Wikipedia error for {title}: {e}")
        return "", ""
    for page in data.get("query", {}).get("pages", {}).values():
        text = page.get("extract") or ""
        if text:
            real = page.get("title", title)
            url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(real.replace(" ", "_"))
            return text[:limit], url
    return "", ""


def _get_page(url, timeout=40):
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


def dcb_bios_of_the_day():
    """Dictionary of Canadian Biography: people born or died on this day (its "biography of the day" page)."""
    page = _get_page("http://www.biographi.ca/en/bio_of_the_day.html")
    out = {}
    for href, name in re.findall(r'href="((?:https?://www\.biographi\.ca)?/en/bio/[A-Za-z0-9_]+\.html)"[^>]*>(.*?)</a>',
                                 page, re.S):
        url = urllib.parse.urljoin("http://www.biographi.ca/", href)
        name = _clean(name, 120)
        if len(name) > 3 and url not in out:
            out[url] = name
    return [{"url": u, "name": n} for u, n in out.items()]


def wiki_on_this_day(d):
    try:
        data = json.loads(http(f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/{d:%m}/{d:%d}"))
    except Exception as e:
        print(f"On-this-day error: {e}")
        return []
    out = []
    for kind in ("selected", "events", "births", "deaths"):
        for e in data.get(kind, []):
            pages = e.get("pages") or []
            blob = e.get("text", "") + " " + " ".join(p.get("extract", "") for p in pages[:2])
            if pages and any(w in blob for w in CANADA_WORDS):
                out.append({"kind": kind, "year": e.get("year"), "text": e.get("text", ""),
                            "page": pages[0].get("title", "")})
    return out


def _write_history(topic, source, article, opening, header, source_name, url, s, stamp, image=""):
    post = parse_post(ask_claude(HISTORY_WRITE_PROMPT.format(
        topic=topic, source=source_name, article=article, opening=opening)))
    if not post:
        print("Could not write the history post")
        return False
    query = post.get("image_query", "")
    edited = parse_post(ask_claude(EDIT_PROMPT.format(
        draft=json.dumps({"title": post["title"], "body": post["body"]}, ensure_ascii=False),
        title=topic, summary="", article=article)))
    post = edited or post
    if not image:  # the source has no usable photo: look for a freely licensed one
        image = commons_image(query)
        print(f"Image from Wikimedia Commons for '{query}': {image or 'none'}")
    text = format_post(post["title"], post["body"], source_name, url, header=header)
    return send_draft(s, url, text, stamp, image=image)


def _history_state():
    if not ADMIN_IDS:
        sys.exit("TELEGRAM_ADMIN_ID is not set")
    s = load_state()
    s.setdefault("history_done", [])
    return s


def _done(s, key):
    s["history_done"].append(key)
    s["history_done"] = s["history_done"][-1000:]


def _date_opening(d, year=""):
    return (f"Start with the date: this happened on this day, {d.day}.{d.month:02d}"
            + (f".{year}" if year else "") + " (write the date in Ukrainian words, e.g. «22 листопада 1902 року»).")


def cmd_thisday():
    """Canadian sources first (Dictionary of Canadian Biography); Wikipedia "On this day" only as a fallback."""
    s = _history_state()
    stamp = now().isoformat()
    d = now().astimezone(LOCAL)
    header = "📅 Цей день в історії Канади"

    bios = [b for b in dcb_bios_of_the_day() if b["url"] not in s["history_done"]]
    print(f"{len(bios)} DCB biographies for {d:%B %d}")
    if bios:
        listing = "\n".join(f"[{i}] (biography: born or died on {d:%B} {d.day}) {b['name']}" for i, b in enumerate(bios))
        for i in parse_picks(ask_claude(THISDAY_PICK_PROMPT.format(items=listing)))[:2]:
            if i >= len(bios):
                continue
            b = bios[i]
            _done(s, b["url"])
            article, image = fetch_page(b["url"], 9000)
            if len(article) < 800:
                continue
            topic = f"{b['name']} (born or died on {d:%B} {d.day}; the text says which, and the year)"
            if _write_history(topic, "Dictionary of Canadian Biography", article,
                              "Start with the date (day, month and year in Ukrainian words, e.g. «22 листопада 1902 року») "
                              "and what happened on it: the person's birth or death.",
                              header, "Dictionary of Canadian Biography", b["url"], s, stamp, image):
                print(f"This-day draft sent: {b['name']} (DCB)")
                return save_state(s)

    # Fallback: Wikipedia "On this day", Canadian entries
    entries = [e for e in wiki_on_this_day(d) if e["page"] not in s["history_done"]]
    print(f"Fallback: {len(entries)} Wikipedia entries")
    if entries:
        listing = "\n".join(f"[{i}] {e['year']} ({e['kind']}): {e['text']}" for i, e in enumerate(entries[:40]))
        for i in parse_picks(ask_claude(THISDAY_PICK_PROMPT.format(items=listing)))[:2]:
            if i >= len(entries):
                continue
            e = entries[i]
            _done(s, e["page"])
            article, url = wiki_text(e["page"])
            if len(article) < 500:
                continue
            image = fetch_page(url)[1]
            if _write_history(f"{e['year']}: {e['text']}", "Вікіпедія", article, _date_opening(d, e["year"]),
                              header, "Вікіпедія", url, s, stamp, image):
                print(f"This-day draft sent: {e['text']} (Wikipedia)")
            break
    save_state(s)


def _story_from(candidates, s, stamp, header):
    """Let Claude rank the candidates, then write the first one that has enough text."""
    listing = "\n".join(f"[{i}] ({c['region']}, {c['source']}) {c['title']}" for i, c in enumerate(candidates))
    for i in parse_picks(ask_claude(STORY_PICK_PROMPT.format(items=listing)))[:3]:
        if i >= len(candidates):
            continue
        c = candidates[i]
        _done(s, c["url"])
        article, image = fetch_page(c["url"], 8000)
        if len(article) < 800:
            print(f"Too little text for {c['title']}; trying the next pick")
            continue
        if _write_history(c["title"], c["source"], article, "Open with a vivid detail or the key moment.",
                          header, c["source"], c["url"], s, stamp, image):
            print(f"History draft sent: {c['title']} ({c['source']})")
            return True
    return False


def _collect(sources, s, per_source=6):
    out = []
    for src in sources:
        links = [(u, t) for u, t in harvest(src) if u not in s["history_done"]]
        for u, t in random.sample(links, min(per_source, len(links))):
            out.append({"url": u, "title": t, "source": src["name"], "region": src["region"]})
    return out


def _wiki_story(titles, s, stamp, header):
    """Fallback: the first unused Wikipedia topic from a list of (region, title)."""
    for region, title in titles:
        if title in s["history_done"]:
            continue
        _done(s, title)
        article, url = wiki_text(title)
        if len(article) < 800:
            continue
        image = fetch_page(url)[1]
        if _write_history(title, "Вікіпедія", article, "Open with a vivid detail or the key moment.",
                          header, "Вікіпедія", url, s, stamp, image):
            print(f"History draft sent: {title} (Wikipedia fallback)")
            return True
    return False


def cmd_history(ukrainian=False):
    """Canadian sources first; Wikipedia only if none of them gives a usable story."""
    s = _history_state()
    stamp = now().isoformat()
    header = "🍁 Історія Канади"
    if ukrainian or now().astimezone(LOCAL).weekday() == config.UKRAINIAN_CANADIAN_DAY:
        candidates = _collect(config.UKRAINIAN_CANADIAN_SOURCES, s, per_source=8)
        print(f"{len(candidates)} Ukrainian-Canadian candidates")
        ok = candidates and _story_from(candidates, s, stamp, header)
        if not ok:
            topics = [("Ukrainian Canadians", t) for t in config.UKRAINIAN_CANADIAN_TOPICS]
            _wiki_story(topics, s, stamp, header)
        return save_state(s)

    sources = random.sample(config.HISTORY_SOURCES, min(4, len(config.HISTORY_SOURCES)))
    candidates = _collect(sources, s)
    print(f"{len(candidates)} candidates")
    if not (candidates and _story_from(candidates, s, stamp, header)):
        _wiki_story(random.sample(config.WIKI_REGIONAL_TOPICS, len(config.WIKI_REGIONAL_TOPICS)), s, stamp, header)
    save_state(s)


def answer(cq, text, alert=False):
    # Telegram rejects answers to taps older than a few minutes; that's harmless.
    try:
        tg("answerCallbackQuery", callback_query_id=cq["id"], text=text, show_alert=alert)
    except Exception as e:
        print(f"(could not answer tap: {e})")


def cmd_approve():
    s = load_state()
    updates = tg("getUpdates", offset=s["tg_offset"], timeout=0,
                 allowed_updates=["callback_query"])
    for u in updates:
        s["tg_offset"] = u["update_id"] + 1
        cq = u.get("callback_query")
        if not cq:
            continue
        if str(cq["from"]["id"]) not in ADMIN_IDS:
            answer(cq, "Not allowed")
            continue
        who = html.escape(str(cq["from"].get("first_name") or cq["from"]["id"]))
        action, _, did = (cq.get("data") or "").partition(":")
        d = s["pending"].get(did)
        if not d:
            answer(cq, "Already handled or expired")
            continue
        if action == "pub":
            try:
                tg("sendMessage", chat_id=config.CHANNEL, text=d["text"], parse_mode="HTML",
                   link_preview_options=d.get("lp") or preview(d["url"]))
            except Exception as e:
                print(f"PUBLISH ERROR: {e}")
                answer(cq, "Publishing failed, check the bot is a channel admin", alert=True)
                continue
            answer(cq, "Published")
            close_draft(d, f"✅ Published by {who}")
            print(f"Published {d['url']}")
        else:
            answer(cq, "Skipped")
            close_draft(d, f"❌ Skipped by {who}")
        del s["pending"][did]
        save_state(s)  # save after every tap so a later error can never cause a double post

    cutoff = (now() - timedelta(hours=config.DRAFT_EXPIRY_HOURS)).isoformat()
    for did, d in list(s["pending"].items()):
        if d["created"] < cutoff:
            close_draft(d, "⌛ Expired")
            del s["pending"][did]
    save_state(s)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "draft":
        cmd_draft()
    elif cmd == "approve":
        cmd_approve()
    elif cmd == "history":
        cmd_history(ukrainian=len(sys.argv) > 2 and sys.argv[2] == "ukrainian")
    elif cmd == "thisday":
        cmd_thisday()
    elif cmd == "merge-state":  # used by save_state.sh: merge-state BASE OURS (theirs = state.json)
        with open(sys.argv[2], encoding="utf-8") as f:
            base = json.load(f)
        with open(sys.argv[3], encoding="utf-8") as f:
            ours = json.load(f)
        save_state(merge_state(base, ours, load_state()))
    else:
        sys.exit("Usage: python bot.py draft|approve|history|thisday")
