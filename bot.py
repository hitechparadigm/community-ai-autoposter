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
from prompts import (AUDIENCE, DIGEST_PROMPT, EDIT_PROMPT, HISTORY_WRITE_PROMPT, PICK_PROMPT,
                     STORY_PICK_PROMPT, STYLE, THISDAY_PICK_PROMPT, WRITE_PROMPT)

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(HERE, "state.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")
# Wikimedia asks bots to identify themselves (and throttles generic browser user agents)
WIKI_UA = "UkrainianCanadaBot/1.0 (https://t.me/UkrainianCanada; Telegram news channel)"
ATOM = "{http://www.w3.org/2005/Atom}"
DC = "{http://purl.org/dc/elements/1.1/}"

TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
# One or more approver IDs, comma-separated (e.g. "456360947,123456789")
ADMIN_IDS = [x.strip() for x in os.environ.get("TELEGRAM_ADMIN_ID", "").split(",") if x.strip()]
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
FB_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "").strip()
FB_TOKEN = os.environ.get("FACEBOOK_PAGE_TOKEN", "").strip()


# ---------- helpers ----------

def now():
    return datetime.now(timezone.utc)


def http(url, data=None, headers=None, timeout=30):
    h = {"User-Agent": WIKI_UA if re.search(r"wiki[mp]edia\.org", url) else UA}
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
    out["digest_regions"] = {**out.get("digest_regions", {}), **ours.get("digest_regions", {})}
    out["ref_index"] = max(theirs.get("ref_index", 0), ours.get("ref_index", 0))
    if ours.get("thisday_last"):
        out["thisday_last"] = ours["thisday_last"]
    if ours.get("telegraph_token") and not out.get("telegraph_token"):
        out["telegraph_token"] = ours["telegraph_token"]
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


def fetch_news(seen, max_age_hours=None, limit=200):
    """Recent items from all feeds that aren't in `seen`, newest first, each tagged with its region."""
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
            community = region != "Ukraine" and any(  # Ukrinform is all about Ukraine: not "community"
                w in it["title"] + " " + it["summary"] for w in config.COMMUNITY_WORDS)
            if taken >= config.ITEMS_PER_FEED and not community:
                continue
            if it["url"] in seen or it["url"] in urls:
                continue
            if it["published"] and it["published"] < cutoff:
                continue
            it["region"] = region
            it["community"] = community or region == "Ukrainian community in Canada"
            urls.add(it["url"])
            items.append(it)
            taken += 1
    items.sort(key=lambda i: (i.get("community", False), i["published"] or now()), reverse=True)
    return items[:limit]


# ---------- Claude ----------


def ask_claude(prompt):
    if not ANTHROPIC_KEY:
        sys.exit("ANTHROPIC_API_KEY is not set")
    raw = http(
        "https://api.anthropic.com/v1/messages",
        {"model": config.MODEL, "max_tokens": 12000,
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


def parse_post(text, keys=("title", "body")):
    post = _json(text, "{", "}")
    if isinstance(post, dict) and all(post.get(k) for k in keys):
        return post
    return None


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
    words = set(re.findall(r"\w+", query.lower()))
    for params in ({"titles": query, "redirects": 1},
                   {"generator": "search", "gsrsearch": query, "gsrlimit": 3}):
        q = urllib.parse.urlencode({"action": "query", "prop": "pageimages", "piprop": "original",
                                    "format": "json", **params})
        try:
            pages = json.loads(http(f"https://en.wikipedia.org/w/api.php?{q}")).get("query", {}).get("pages", {})
        except Exception as e:
            print(f"Commons image search failed: {e}")
            return ""
        for p in sorted(pages.values(), key=lambda p: p.get("index", 0)):
            title = set(re.findall(r"\w+", p.get("title", "").lower()))
            src = (p.get("original") or {}).get("source", "")
            if src and words <= title and not BAD_IMG.search(src) and image_ok(src):
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
        f"[{i}] {'[UKRAINIAN COMMUNITY] ' if it.get('community') else ''}({it['region']}, {it['source']}) "
        f"{it['title']} — {it['summary'][:200]}" for i, it in enumerate(items))
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


def send_draft(s, url, text, stamp, image="", preview_url=""):
    """Send a draft with Publish/Skip buttons to every approver and remember it.
    With an image, the picture is shown above the post (via an invisible link) instead of the source preview."""
    did = hashlib.sha1(url.encode()).hexdigest()[:10]
    if preview_url:
        lp = {"url": preview_url, "prefer_large_media": True, "show_above_text": True}
    elif image:
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


# ---------- daily digest ----------

def outlet(source):
    """Media outlet from a feed name: "CBC Manitoba" -> "CBC", "Global News Winnipeg" -> "Global News"."""
    for name in ("CBC", "Global News"):
        if source.startswith(name):
            return name
    return source


UK_MONTHS = ["січня", "лютого", "березня", "квітня", "травня", "червня", "липня", "серпня",
             "вересня", "жовтня", "листопада", "грудня"]


def cmd_digest():
    if not ADMIN_IDS:
        sys.exit("TELEGRAM_ADMIN_ID is not set")
    s = load_state()
    s.setdefault("digest_regions", {})
    d = now().astimezone(LOCAL)
    items = [it for it in fetch_news({}, max_age_hours=36, limit=250) if it["region"] != "Ukraine"]
    print(f"{len(items)} items for the digest")
    if len(items) < 5:
        return save_state(s)
    recent = sorted(s["digest_regions"], key=lambda r: s["digest_regions"][r], reverse=True)[:6]
    listing = "\n".join(
        f"[{i}] {'[UKRAINIAN COMMUNITY] ' if it.get('community') else ''}({it['region']}, {it['source']}, "
        f"{it['published'].astimezone(LOCAL).strftime('%a %b %d %H:%M') if it['published'] else '?'}) "
        f"{it['title']} — {it['summary'][:200]}" for i, it in enumerate(items))
    prompt = DIGEST_PROMPT.format(national=config.DIGEST_NATIONAL, regions=config.DIGEST_REGIONS,
                                  recent=", ".join(recent) or "none", items=listing, today=f"{d:%A, %B %d, %Y}")
    digest = _json(ask_claude(prompt), "{", "}")
    if not isinstance(digest, dict) or not digest.get("national"):
        sys.exit("Could not write the digest")
    edited = _json(ask_claude(EDIT_PROMPT.format(
        draft=json.dumps(digest, ensure_ascii=False), title="Daily news digest", summary="",
        article="\n".join(f"{it['title']} — {it['summary']}" for it in items))), "{", "}")
    if isinstance(edited, dict) and edited.get("national"):
        digest = edited

    e = html.escape

    used = []

    def line(entry):
        try:
            it = items[int(entry["id"])]
        except (KeyError, ValueError, IndexError, TypeError):
            return ""
        used.append(outlet(it["source"]))
        text = entry.get("text", "")
        link = f'<a href="{e(it["url"], quote=True)}">'
        m = re.search(r"\[([^\]]+)\]", text)
        if not m:  # no marked phrase: link the first few words
            m = re.match(r"\s*((?:\S+\s+){0,3}\S+)", text)
        if not m:
            return ""
        before, phrase, after = text[:m.start()], m.group(1), text[m.end():].replace("[", "").replace("]", "")
        return f"• {e(before, quote=False)}{link}{e(phrase, quote=False)}</a>{e(after, quote=False)}"

    y = d - timedelta(days=1)
    parts = [f"🗞 <b>Головне за вчора · {y.day} {UK_MONTHS[y.month - 1]}</b>", "", "🇨🇦 <b>Канада</b>"]
    parts += [l for l in map(line, digest["national"]) if l]
    for reg in digest.get("regions", []):
        lines = [l for l in map(line, reg.get("items", [])) if l]
        if lines:
            parts += ["", f"📍 <b>{e(reg.get('region', ''), quote=False)}</b>"] + lines
            s["digest_regions"][reg.get("region_en") or reg.get("region", "")] = d.strftime("%Y-%m-%d")
    community_lines = [l for l in map(line, digest.get("community") or []) if l]
    if community_lines:
        parts += ["", "🇺🇦 <b>Українська громада</b>"] + community_lines
    today_lines = [l for l in map(line, digest.get("today") or []) if l]
    if today_lines:
        parts += ["", f"📌 <b>Сьогодні, {d.day} {UK_MONTHS[d.month - 1]}</b>"] + today_lines
    outlets = list(dict.fromkeys(used))
    parts += ["", f"<i>За матеріалами: {e(', '.join(outlets), quote=False)}</i>",
              f"<a href=\"{config.TELEGRAPH_AUTHOR_URL}\">{e(config.TELEGRAPH_AUTHOR, quote=False)}</a>"]
    refs = getattr(config, "REFERRALS", [])
    if refs:  # one referral link per digest, rotating
        label, link = refs[s.get("ref_index", 0) % len(refs)][:2]
        s["ref_index"] = s.get("ref_index", 0) + 1
        parts += ["", f"<a href=\"{e(link, quote=True)}\">{e(label, quote=False)}</a>"]
        if config.REFERRAL_DISCLOSURE:
            parts.append(f"<i>{e(config.REFERRAL_DISCLOSURE, quote=False)}</i>")
    text = "\n".join(parts)[:4000]
    try:
        top = items[int(digest["national"][0]["id"])]["url"]
    except (KeyError, ValueError, IndexError, TypeError):
        top = ""
    key = f"digest:{d:%Y-%m-%d}"
    if send_draft(s, key, text, now().isoformat(), preview_url=top):
        print("Digest draft sent")
    save_state(s)


# ---------- Canadian history ----------
# Two daily columns, both approved like the news:
#   "📅 Цей день в історії Канади" (python bot.py thisday) - an event, birth or death on today's date
#   "🍁 Історія Канади"            (python bot.py history) - a story from the history sources in config.py


LOCAL = timezone(timedelta(hours=-5))  # Toronto (standard time is close enough for picking a date)


def wiki_text(title, limit=15000):
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
            if pages and any(w in blob for w in config.CANADA_WORDS):
                out.append({"kind": kind, "year": e.get("year"), "text": e.get("text", ""),
                            "page": pages[0].get("title", "")})
    return out


def telegraph(method, s, **params):
    """Call the Telegraph API (telegra.ph). The bot creates its own account once and keeps the token in state."""
    if method != "createAccount" and not s.get("telegraph_token"):
        acc = telegraph("createAccount", s, short_name="UkrainianCanada", author_name=config.TELEGRAPH_AUTHOR,
                        author_url=config.TELEGRAPH_AUTHOR_URL)
        s["telegraph_token"] = acc["access_token"]
    if method != "createAccount":
        params["access_token"] = s["telegraph_token"]
    resp = json.loads(http(f"https://api.telegra.ph/{method}", params))
    if not resp.get("ok"):
        raise RuntimeError(f"Telegraph {method} failed: {resp}")
    return resp["result"]


def telegraph_nodes(body, image, image_credit, source_name, url):
    """Turn the article text into Telegraph content: photo, paragraphs, subheadings, source."""
    nodes = []
    if image:
        nodes.append({"tag": "figure", "children": [{"tag": "img", "attrs": {"src": image}},
                                                    {"tag": "figcaption", "children": [f"Фото: {image_credit}"]}]})
    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if block.startswith("#"):
            nodes.append({"tag": "h4", "children": [block.lstrip("# ").strip()]})
        elif block:
            nodes.append({"tag": "p", "children": [block]})
    nodes.append({"tag": "hr"})
    nodes.append({"tag": "p", "children": ["Джерело: ", {"tag": "a", "attrs": {"href": url}, "children": [source_name]}]})
    nodes.append({"tag": "p", "children": [{"tag": "a", "attrs": {"href": config.TELEGRAPH_AUTHOR_URL},
                                            "children": [config.TELEGRAPH_AUTHOR]}]})
    return nodes


def _write_history(topic, source, article, opening, header, source_name, url, s, stamp, image=""):
    """Write a long-read, publish it on Telegraph, and send the teaser post as a draft."""
    keys = ("title", "teaser", "body")
    post = parse_post(ask_claude(HISTORY_WRITE_PROMPT.format(
        topic=topic, source=source_name, article=article, opening=opening)), keys)
    if not post:
        print("Could not write the history post")
        return False
    query = (post.get("image_query") or "").strip()
    if not query and not image:  # ask separately: the English Wikipedia title of the main subject
        query = ask_claude("Give the exact English Wikipedia article title for the main person, place or event "
                           f"of this story: {topic}\nReply with the title only.").strip().strip('"')[:100]
    edited = parse_post(ask_claude(EDIT_PROMPT.format(
        draft=json.dumps({k: post[k] for k in keys}, ensure_ascii=False),
        title=topic, summary="", article=article)), keys)
    post = edited or post
    credit = source_name
    if not image:  # the source has no usable photo: look for a freely licensed one
        image = commons_image(query)
        credit = "Wikimedia Commons"
        print(f"Image from Wikimedia Commons for '{query}': {image or 'none'}")
    try:
        page = telegraph("createPage", s, title=post["title"][:256], author_name=config.TELEGRAPH_AUTHOR,
                         author_url=config.TELEGRAPH_AUTHOR_URL,
                         content=json.dumps(telegraph_nodes(post["body"], image, credit, source_name, url),
                                            ensure_ascii=False))
    except Exception as e:  # Telegraph down: fall back to a normal post
        print(f"Telegraph error, sending a normal post instead: {e}")
        text = format_post(post["title"], post["teaser"] + "\n\n" + post["body"].replace("## ", ""),
                           source_name, url, header=header)
        return send_draft(s, url, text[:4000], stamp, image=image)
    e = html.escape
    text = (f"{e(header, quote=False)}\n\n<b>{e(post['title'], quote=False)}</b>\n\n{e(post['teaser'], quote=False)}"
            f"\n\n📖 <b><a href=\"{e(page['url'], quote=True)}\">Читати повністю →</a></b>")
    # the source is credited at the end of the Telegraph article, not in the post
    print(f"Telegraph page: {page['url']}")
    ok = send_draft(s, url, text, stamp, preview_url=page["url"])
    if ok:
        s["pending"][hashlib.sha1(url.encode()).hexdigest()[:10]]["telegraph_path"] = page["path"]
    return ok


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
    """An event or a person on today's date, alternating day by day.
    People: Dictionary of Canadian Biography. Events: Wikipedia "On this day" (Canadian entries) - the
    Canadian sites with dated events (The Canadian Encyclopedia) block automated access."""
    s = _history_state()
    stamp = now().isoformat()
    d = now().astimezone(LOCAL)
    header = "📅 Цей день в історії Канади"
    want = "event" if s.get("thisday_last") != "event" else "person"

    cands = [{"kind": "person", "label": f"person (born or died on {d:%B} {d.day}): {b['name']}", **b}
             for b in dcb_bios_of_the_day() if b["url"] not in s["history_done"]]
    for e in wiki_on_this_day(d):
        if e["page"] not in s["history_done"]:
            kind = "event" if e["kind"] in ("selected", "events") else "person"
            cands.append({"kind": kind, "label": f"{kind} ({e['year']}): {e['text']}", "wiki": e})
    print(f"{len(cands)} candidates for {d:%B %d}; today prefers: {want}")
    if not cands:
        return save_state(s)
    listing = "\n".join(f"[{i}] {c['label']}" for i, c in enumerate(cands[:60]))
    prompt = THISDAY_PICK_PROMPT.format(items=listing) + (
        f"\nToday choose {'an EVENT (something that happened)' if want == 'event' else 'a PERSON'} "
        "if there is a good one; otherwise the best entry of any kind. Return up to 3 ids, best first.")
    for i in parse_picks(ask_claude(prompt))[:3]:
        if i >= len(cands):
            continue
        c = cands[i]
        if "wiki" in c:
            e = c["wiki"]
            _done(s, e["page"])
            article, url = wiki_text(e["page"])
            if len(article) < 500:
                continue
            ok = _write_history(f"{e['year']}: {e['text']}", "Вікіпедія", article, _date_opening(d, e["year"]),
                                header, "Вікіпедія", url, s, stamp, fetch_page(url)[1])
        else:
            _done(s, c["url"])
            article, image = fetch_page(c["url"], 15000)
            if len(article) < 800:
                continue
            ok = _write_history(f"{c['name']} (born or died on {d:%B} {d.day}; the text says which, and the year)",
                                "Dictionary of Canadian Biography", article,
                                "Start with the date (day, month and year in Ukrainian words, e.g. «22 листопада 1902 року») "
                                "and what happened on it: the person's birth or death.",
                                header, "Dictionary of Canadian Biography", c["url"], s, stamp, image)
        if ok:
            s["thisday_last"] = c["kind"]
            print(f"This-day draft sent ({c['kind']}): {c['label']}")
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
        article, image = fetch_page(c["url"], 15000)
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


def retire_telegraph(d, s):
    """A long-read that won't be published: replace its Telegraph page with a short notice."""
    if not d.get("telegraph_path"):
        return
    try:
        telegraph("editPage", s, path=d["telegraph_path"], title="Матеріал не опубліковано",
                  content=json.dumps([{"tag": "p", "children": ["Цей матеріал не опубліковано."]}],
                                     ensure_ascii=False))
    except Exception as e:
        print(f"Could not retire Telegraph page: {e}")


def fb_text(text):
    """Telegram HTML -> plain text for Facebook (links written out, since Facebook ignores HTML)."""
    text = re.sub(r'<a href="[^"]*">&#8203;</a>', "", text)  # invisible image link

    def link(m):
        url = html.unescape(m.group(1)).replace("?cmp=rss", "")
        label = html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        if "Читати повністю" in label:
            return f"📖 Читати повністю: {url}"
        if url.startswith("https://t.me/"):
            return label
        return f"{label} ({url})"

    text = re.sub(r'<a href="([^"]+)">(.*?)</a>', link, text, flags=re.S)
    text = html.unescape(re.sub(r"</?(b|i|u|s)>", "", text))
    return text.replace("📖 📖", "📖").strip()


def post_to_facebook(d):
    """Publish an approved post to the Facebook Page (only if the Facebook secrets are set)."""
    if not (FB_PAGE_ID and FB_TOKEN):
        return None
    lp_url = (d.get("lp") or {}).get("url", "")
    link = lp_url if lp_url and not re.search(r"\.(jpe?g|png|webp)(\?|$)", lp_url, re.I) else d["url"]
    params = {"message": fb_text(d["text"]), "access_token": FB_TOKEN}
    if link.startswith("http"):
        params["link"] = link.replace("?cmp=rss", "")
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f"https://graph.facebook.com/{FB_PAGE_ID}/feed", data=data,
                                 headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read()).get("id", "ok")
    except urllib.error.HTTPError as e:
        raise RuntimeError(e.read().decode(errors="replace")[:300]) from None


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
            fb = ""
            try:
                if post_to_facebook(d):
                    fb = " + Facebook"
            except Exception as e:
                print(f"FACEBOOK ERROR: {e}")
                fb = " (Facebook failed: check the token)"
            answer(cq, "Published" + fb)
            close_draft(d, f"✅ Published by {who}{fb}")
            print(f"Published {d['url']}")
        else:
            answer(cq, "Skipped")
            close_draft(d, f"❌ Skipped by {who}")
            retire_telegraph(d, s)
        del s["pending"][did]
        save_state(s)  # save after every tap so a later error can never cause a double post

    cutoff = (now() - timedelta(hours=config.DRAFT_EXPIRY_HOURS)).isoformat()
    for did, d in list(s["pending"].items()):
        if d["created"] < cutoff:
            close_draft(d, "⌛ Expired")
            retire_telegraph(d, s)
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
    elif cmd == "digest":
        cmd_digest()
    elif cmd == "merge-state":  # used by save_state.sh: merge-state BASE OURS (theirs = state.json)
        with open(sys.argv[2], encoding="utf-8") as f:
            base = json.load(f)
        with open(sys.argv[3], encoding="utf-8") as f:
            ours = json.load(f)
        save_state(merge_state(base, ours, load_state()))
    else:
        sys.exit("Usage: python bot.py draft|approve|history|thisday|digest")
