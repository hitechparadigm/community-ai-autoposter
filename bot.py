#!/usr/bin/env python3
"""Community AI autoposter (settings: config.py, editorial instructions: prompts.py).

  python bot.py draft    - fetch news, have Claude pick and write posts,
                           send drafts to you in Telegram with Publish / Skip buttons
  python bot.py digest   - draft the morning digest
  python bot.py thisday  - draft one "This day in history" post
  python bot.py history  - draft one history story ("history community" = a community-history story)
  python bot.py tick     - every 5 minutes: run what's due by config.SCHEDULE, then publish approved posts
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
from zoneinfo import ZoneInfo

import config
from prompts import (COMMUNITY_FOCUS, AUDIENCE, DIGEST_PROMPT, EDIT_PROMPT, FIX_PROMPT, REVIEW_PROMPT, HISTORY_WRITE_PROMPT, PICK_PROMPT,
                     REFERRAL_MATCH_PROMPT, STORY_PICK_PROMPT, STYLE, THISDAY_PICK_PROMPT, WRITE_PROMPT,
                     DATE_WORDS)

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(HERE, "state.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")
# Wikimedia asks bots to identify themselves (and throttles generic browser user agents)
WIKI_UA = f"{config.BOT_NAME}/1.0 ({config.BOT_CONTACT_URL})"
ATOM = "{http://www.w3.org/2005/Atom}"
DC = "{http://purl.org/dc/elements/1.1/}"

TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
# One or more approver IDs, comma-separated (e.g. "456360947,123456789")
ADMIN_IDS = [x.strip() for x in os.environ.get("TELEGRAM_ADMIN_ID", "").split(",") if x.strip()]
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
TELEGRAPH_TOKEN = os.environ.get("TELEGRAPH_TOKEN", "").strip()
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
    out["schedule_done"] = {**out.get("schedule_done", {}), **ours.get("schedule_done", {})}
    rn_t, rn_o = theirs.get("ref_news", {}), ours.get("ref_news", {})
    out["ref_news"] = max((rn_t, rn_o), key=lambda r: (r.get("date", ""), r.get("count", 0)))
    if ours.get("thisday_last"):
        out["thisday_last"] = ours["thisday_last"]
    out.pop("telegraph_token", None)
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


def fetch_news(seen, max_age_hours=None, limit=150):
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
            community = region not in config.NOT_COMMUNITY_REGIONS and any(
                w in it["title"] + " " + it["summary"] for w in config.COMMUNITY_WORDS)
            if taken >= config.ITEMS_PER_FEED and not community:
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


# ---------- Claude ----------


SOURCE_REF = "(the source text is at the beginning of this message)"
_usage = {"calls": 0, "input": 0, "cache_read": 0, "cache_write": 0, "output": 0}


def schema_post(keys, optional=()):
    """Tool schema for a post with these text fields."""
    return {"type": "object", "properties": {k: {"type": "string"} for k in (*keys, *optional)},
            "required": list(keys)}


SCHEMA_IDS = {"type": "object", "properties": {"ids": {"type": "array", "items": {"type": "integer"}}},
              "required": ["ids"]}
SCHEMA_REVIEW = {"type": "object", "properties": {
    "verdict": {"type": "string", "enum": ["ok", "fix"]},
    "problems": {"type": "array", "items": {"type": "string"}}}, "required": ["verdict"]}
SCHEMA_REFERRAL = {"type": "object", "properties": {"id": {"type": ["integer", "null"]}}, "required": ["id"]}
_ITEMS = {"type": "array", "items": {"type": "object", "properties": {
    "id": {"type": "integer"}, "text": {"type": "string"}}, "required": ["id", "text"]}}
SCHEMA_DIGEST = {"type": "object", "properties": {
    "national": _ITEMS,
    "regions": {"type": "array", "items": {"type": "object", "properties": {
        "region": {"type": "string"}, "region_en": {"type": "string"}, "items": _ITEMS},
        "required": ["region", "items"]}},
    "community": _ITEMS, "today": _ITEMS}, "required": ["national"]}


def ask_claude(prompt, source=None, schema=None):
    """One Claude call. With `source`, the source text goes first as a cached block: the writer, copy editor,
    reviewer and fixer all send the same source within a minute, so later calls read it from the cache at a
    fraction of the price (prompts then refer to it with SOURCE_REF instead of repeating it)."""
    if not ANTHROPIC_KEY:
        sys.exit("ANTHROPIC_API_KEY is not set")
    if source:
        content = [{"type": "text", "text": f"SOURCE TEXT:\n{source}", "cache_control": {"type": "ephemeral"}},
                   {"type": "text", "text": prompt}]
    else:
        content = prompt
    body = {"model": config.MODEL, "max_tokens": 12000, "messages": [{"role": "user", "content": content}]}
    if schema:  # structured answer through tool use: always well-formed JSON, no parsing guesswork
        body["tools"] = [{"name": "answer", "description": "Return the answer in this structure.",
                          "input_schema": schema}]
        body["tool_choice"] = {"type": "auto"}  # this model doesn't allow forcing a tool; the prompt asks for it
        content_last = body["messages"][0]["content"]
        note = "\n\nGive your answer by calling the `answer` tool."
        if isinstance(content_last, list):
            content_last[-1]["text"] += note
        else:
            body["messages"][0]["content"] = content_last + note
    raw = http(
        "https://api.anthropic.com/v1/messages",
        body,
        {"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01"},
        timeout=180,
    )
    resp = json.loads(raw)
    u = resp.get("usage", {})
    _usage["calls"] += 1
    for k, f in (("input", "input_tokens"), ("cache_read", "cache_read_input_tokens"),
                 ("cache_write", "cache_creation_input_tokens"), ("output", "output_tokens")):
        _usage[k] += u.get(f) or 0
    if schema:
        for b in resp.get("content", []):
            if b.get("type") == "tool_use":
                data = b.get("input", {})
                return json.dumps(data["ids"] if list(data) == ["ids"] else data, ensure_ascii=False)
        print("(no tool call in the answer; reading the text instead)")  # the text parsers still work
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


# Latin letters that look like Cyrillic ones; models sometimes mix them into Ukrainian words
HOMOGLYPHS = str.maketrans("aceiopxyACEHIKMOPTXB", "асеіорхуАСЕНІКМОРТХВ")
# A real glitch: Cyrillic letters glued to a run of Latin letters, e.g. "машaccording"
BROKEN_WORD = re.compile(r"[а-яіїєґ][a-z]{3,}|[a-z]{3,}[а-яіїєґ]", re.I)


def fix_homoglyphs(text):
    """Replace look-alike Latin letters inside Ukrainian words with the Cyrillic ones."""
    text = re.sub(r"\b\w*[а-яіїєґ]\w*\b",
                  lambda m: m.group(0).translate(HOMOGLYPHS) if re.search(r"[a-z]", m.group(0), re.I) else m.group(0),
                  text, flags=re.I)
    # the conjunction "і" typed with a Latin "i" between Ukrainian words
    return re.sub(r"(?<=[а-яіїєґ,»)]\s)([iI])(?=\s+[а-яіїєґ«(])",
                  lambda m: "і" if m.group(1) == "i" else "І", text, flags=re.I)


def edit_ok(original, edited, min_ratio=0.7):
    """Accept the copy editor's version only if it is complete: not much shorter than the original,
    ending like a finished sentence, and without broken words (Latin letters glued to Cyrillic ones)."""
    if not edited:
        return False
    for k, v in original.items():
        if not isinstance(v, str) or k == "image_query":
            continue
        new = edited.get(k, "")
        if not isinstance(new, str) or len(new) < min_ratio * len(v):
            print(f"Copy edit rejected: '{k}' came back cut short")
            return False
        m = BROKEN_WORD.search(new)
        if m:
            print(f"Copy edit rejected: broken word in '{k}': …{new[max(0, m.start() - 20):m.end() + 20]}…")
            return False
        if k in ("body", "teaser") and not re.search(r"[.!?…»)\"]\s*$", new.strip()):
            print(f"Copy edit rejected: '{k}' doesn't end with a full sentence")
            return False
    return True


def review_post(post, keys, article, topic):
    """Reviewer agent: checks the draft against its source; fixes it once if needed and checks again.
    Returns (post, remaining problems)."""
    def review(p):
        r = _json(ask_claude(REVIEW_PROMPT.format(
            topic=topic, draft=json.dumps({k: p[k] for k in keys}, ensure_ascii=False), article=SOURCE_REF),
            source=article, schema=SCHEMA_REVIEW),
            "{", "}") or {}
        return [] if r.get("verdict") == "ok" else [str(x) for x in (r.get("problems") or ["unspecified"])]

    problems = review(post)
    if not problems:
        print("Review: ok")
        return post, []
    print("Review found:", "; ".join(problems))
    fixed = parse_post(ask_claude(FIX_PROMPT.format(
        problems="\n".join(f"- {p}" for p in problems),
        draft=json.dumps({k: post[k] for k in keys}, ensure_ascii=False), article=SOURCE_REF),
        source=article, schema=schema_post(keys)), keys)
    if not fixed or not edit_ok({k: post[k] for k in keys}, fixed, min_ratio=0.3):
        print("Review: the fix came back unusable; keeping the draft and flagging it")
        return post, problems
    fixed = {**post, **{k: fixed[k] for k in keys}}
    left = review(fixed)
    print("Review after fix:", "ok" if not left else "; ".join(left))
    return fixed, left


def review_note(problems):
    """A short warning for the approvers (never published)."""
    if not problems:
        return ""
    items = "\n".join(f"• {html.escape(p)}" for p in problems[:4])
    return f"\n\n<i>⚠️ {html.escape(config.LABELS['review_warning'])}:\n{items}</i>"


def write_long(prompt, keys, tries=2, source=None, optional=()):
    """Ask Claude for a post; if it comes back cut off or garbled, ask again."""
    post = None
    for _ in range(tries):
        post = parse_post(ask_claude(prompt, source=source, schema=schema_post(keys, optional)), keys)
        if post and edit_ok({k: post[k] for k in keys}, post):
            return post
        print("Draft came back incomplete; asking again")
    return post


def parse_post(text, keys=("title", "body")):
    post = _json(text, "{", "}")
    if isinstance(post, dict):
        post = {k: fix_homoglyphs(v) if isinstance(v, str) and k != "image_query" else v for k, v in post.items()}
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
    return fetch_page(url, limit)[0]


# ---------- posts ----------

def format_post(title, body, source, url, header=""):
    e = html.escape
    top = f"{e(header, quote=False)}\n\n" if header else ""
    return (f"{top}<b>{e(title, quote=False)}</b>\n\n{e(body, quote=False)}\n\n"
            f"🔗 {e(config.LABELS['source'])}: <a href=\"{e(url, quote=True)}\">{e(source)}</a>")


def buttons(did):
    return {"inline_keyboard": [[
        {"text": "✅ Publish", "callback_data": f"pub:{did}"},
        {"text": "❌ Skip", "callback_data": f"skip:{did}"},
    ]]}


def preview(url):
    return {"url": url, "prefer_large_media": True}


def admin_key(admin_id):
    """A short, non-reversible label for an approver, so their Telegram ID isn't stored in state.json."""
    return hashlib.sha256(f"approver:{admin_id}".encode()).hexdigest()[:10]


def close_draft(d, status):
    """On every approver's copy of the draft, replace the buttons with a status line."""
    by_key = {admin_key(a): a for a in ADMIN_IDS}
    msgs = d.get("msgs") or [[ADMIN_IDS[0], d["admin_msg_id"]]]  # older drafts stored one id
    for who, msg_id in msgs:
        chat_id = by_key.get(who, who if who in ADMIN_IDS else None)
        if not chat_id:
            continue
        try:
            tg("editMessageText", chat_id=chat_id, message_id=msg_id,
               text=d["text"] + f"\n\n— {status}", parse_mode="HTML",
               link_preview_options={"is_disabled": True})
        except Exception as e:
            print(f"Could not update a draft message: {e}")


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
        f"{it['title']} — {it['summary'][:120]}" for i, it in enumerate(items))
    picks = parse_picks(ask_claude(PICK_PROMPT.format(n=config.DRAFTS_PER_RUN, items=listing), schema=SCHEMA_IDS))
    print(f"Claude picked {picks}")

    stamp = now().isoformat()
    for it in items:  # don't offer the same stories again next run
        s["seen"][it["url"]] = stamp

    for i in picks[:config.DRAFTS_PER_RUN]:
        if i >= len(items):
            continue
        it = items[i]
        article = fetch_article(it["url"])
        src_text = article or "(not available)"
        post = parse_post(ask_claude(WRITE_PROMPT.format(
            source=it["source"], title=it["title"], summary=it["summary"], article=SOURCE_REF), source=src_text,
            schema=schema_post(("title", "body"), ("image_query", "emoji"))))
        if not post:
            print(f"Could not write post for: {it['title']}")
            continue
        photo_query = (post.pop("image_query", "") or "").strip()  # for the Facebook card
        emoji = (post.pop("emoji", "") or "").strip()[:4]  # shown before the headline
        edited = parse_post(ask_claude(EDIT_PROMPT.format(
            draft=json.dumps(post, ensure_ascii=False), title=it["title"],
            summary=it["summary"], article=SOURCE_REF), source=src_text, schema=schema_post(("title", "body"))))
        if edit_ok(post, edited):
            post = edited
        else:
            print("Copy edit failed; using the first draft")
        post, problems = review_post(post, ("title", "body"), article or it["summary"], it["title"])
        text = format_post(f"{emoji} {post['title']}".strip(), post["body"], it["source"], it["url"])
        ref = matching_referral(s, post)
        if ref:
            text += f'\n\n<a href="{html.escape(ref[1], quote=True)}">{html.escape(ref[0], quote=False)}</a>'
        region, fallback = getattr(config, "REGIONS", {}).get(it["region"], (it["region"], ""))
        community = it.get("community")
        card = {"kind": "community" if community else "news", "title": post["title"],
                "tag": config.CARD.get("community_tag", region) if community else region,
                "queries": [*split_queries(photo_query), fallback]}
        if not send_draft(s, it["url"], text, stamp, note=review_note(problems), card=card):
            continue
        if ref:
            s["pending"][hashlib.sha1(it["url"].encode()).hexdigest()[:10]]["referral"] = True
        print(f"Draft sent: {it['title']}")
    save_state(s)


def auto_publish_on(kind):
    return bool(getattr(config, "AUTO_PUBLISH", {}).get(kind))


# ---------- Facebook picture cards ----------

def multipart(fields, files):
    """Encode a multipart/form-data body. files: {name: (filename, bytes, content type)}."""
    boundary = "----autoposter" + hashlib.sha1(os.urandom(8)).hexdigest()
    out = b""
    for k, v in fields.items():
        out += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n").encode()
    for k, (fname, data, ctype) in files.items():
        out += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{fname}\"\r\n"
                f"Content-Type: {ctype}\r\n\r\n").encode() + data + b"\r\n"
    return out + f"--{boundary}--\r\n".encode(), f"multipart/form-data; boundary={boundary}"


def post_multipart(url, fields, files, timeout=60):
    body, ctype = multipart(fields, files)
    req = urllib.request.Request(url, data=body, headers={"Content-Type": ctype, "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(e.read().decode(errors="replace")[:300]) from None


def wiki_thumb(url, width=1280):
    """A smaller copy of a Wikimedia image (originals can be tens of megabytes)."""
    url = url.split("?")[0]
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/(?:commons|en))/(\w/\w\w)/([^/?#]+)$", url)
    if not m or url.lower().endswith(".svg"):
        return url
    return f"{m.group(1)}/thumb/{m.group(2)}/{m.group(3)}/{width}px-{m.group(3)}"


def card_photo(url):
    """Only freely licensed photos go on cards (news outlets' photos are copyrighted)."""
    if not url or not any(d in url for d in config.CARD.get("photo_domains", ("wikimedia.org",))):
        return ""
    if NOT_A_PHOTO.search(urllib.parse.unquote(url.split("?")[0].rsplit("/", 1)[-1])):  # maps, flags, charts
        return ""
    return url


NOT_A_PHOTO = re.compile(r"\.png$|\.svg|map|census|flag|coat_of_arms|seal|diagram|chart|logo|locator", re.I)


MAPLE_LEAF = ("m-90 2030 45-863a95 95 0 0 0-111-98l-859 151 116-320a65 65 0 0 0-20-73l-941-762 212-99a65 65 0 0 0 "
              "34-79l-186-572 542 115a65 65 0 0 0 73-38l105-247 423 454a65 65 0 0 0 111-57l-204-1052 327 189a65 65 "
              "0 0 0 91-27l332-652 332 652a65 65 0 0 0 91 27l327-189-204 1052a65 65 0 0 0 111 57l423-454 105 247a65 "
              "65 0 0 0 73 38l542-115-186 572a65 65 0 0 0 34 79l212 99-941 762a65 65 0 0 0-20 73l116 320-859-151a95 "
              "95 0 0 0-111 98l45 863z")  # the leaf from the Flag of Canada (public domain)


def render_card(card):
    """Draw a Facebook picture card from card.html with headless Chrome. Returns PNG bytes, or b"" if it can't."""
    import base64, shutil, subprocess, tempfile
    chrome = next((c for c in ("google-chrome", "chromium", "chromium-browser") if shutil.which(c)), None)
    tpl = os.path.join(os.path.dirname(os.path.abspath(__file__)), "card.html")
    if not chrome or not os.path.exists(tpl):
        print("Card skipped: Chrome or card.html not found")
        return b""
    c, e = config.CARD, html.escape
    w, h = c["size"]
    d = now().astimezone(LOCAL)
    background = credit = ""
    photo = card_photo(card.get("photo", ""))
    if photo:
        try:
            data = http(wiki_thumb(photo), timeout=40)
            mime = "image/png" if data[:4] == b"\x89PNG" else "image/jpeg"
            background = (f'<div class="photo" style="background-image:url(data:{mime};base64,'
                          f'{base64.b64encode(data).decode()})"></div>')
            who = card.get("credit") or ("Wikimedia Commons" if "wikimedia.org" in photo
                                         else urllib.parse.urlparse(photo).netloc.replace("www.", ""))
            credit = f'<div class="credit">{e(config.LABELS["photo"])}: {e(who)}</div>'
        except Exception as ex:
            print(f"Card photo failed, using the plain background: {ex}")
    kind = card.get("kind", "news")
    items = ""
    if card.get("items"):
        items = "<ol>" + "".join(f"<li>{e(i)}</li>" for i in card["items"]) + "</ol>"
    bigdate = ""
    if kind == "thisday":
        bigdate = f'<div class="bigdate">{d.day}<small>{e(config.MONTHS[d.month - 1])}</small></div>'
    tag = f'<div class="tag">{e(card["tag"])}</div>' if card.get("tag") else ""
    values = {"kind": kind, "layout": "withphoto" if background else "nophoto", "background": background, "credit": credit, "items": items, "bigdate": bigdate,
              "tag": tag, "title": e(card.get("title", "")), "brand": e(c["brand"]),
              "date": f"{d.day} {config.MONTHS[d.month - 1]} {d.year}", "handle": e(c.get("handle", "")),
              "handle2": e(c.get("handle2", "")), "width": w, "height": h, "band": c.get("band", 0),
              "band_color": c.get("band_color", "#A51D18"), **c.get("colors", {})}
    leaf = f'<path d="{MAPLE_LEAF}"/>'
    values["leaves"] = (f'<svg class="leaf-l" viewBox="-2015 -2000 4030 4030">{leaf}</svg>'
                        f'<svg class="leaf-r" viewBox="-2015 -2000 4030 4030">{leaf}</svg>') if c.get("band") else ""
    page = open(tpl, encoding="utf-8").read()
    for k, v in values.items():
        page = page.replace("{{" + k + "}}", str(v))
    with tempfile.TemporaryDirectory() as tmp:
        src, out = os.path.join(tmp, "card.html"), os.path.join(tmp, "card.png")
        open(src, "w", encoding="utf-8").write(page)
        try:
            subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", f"--window-size={w + 2 * c.get('band', 0)},{h}",
                            "--virtual-time-budget=15000", f"--screenshot={out}", src],
                           capture_output=True, timeout=90)
            return open(out, "rb").read()
        except Exception as ex:
            print(f"Card rendering failed: {ex}")
            return b""


def send_card(png, caption="Facebook"):
    """Show the card to the approvers in Telegram; Telegram also stores it until it's published."""
    file_id = ""
    for admin in ADMIN_IDS:
        try:
            fields = {"chat_id": admin, "caption": caption}
            if file_id:  # already uploaded once: reuse it
                tg("sendPhoto", photo=file_id, **fields)
                continue
            r = post_multipart(f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto", fields,
                               {"photo": ("card.png", png, "image/png")})
            file_id = r["result"]["photo"][-1]["file_id"]
        except Exception as ex:
            print(f"Could not send the card to approver #{ADMIN_IDS.index(admin) + 1}: {ex}")
    return file_id


def make_card(card):
    """Render and store a card for Facebook. Only when Facebook is set up (or CARDS_ALWAYS for testing)."""
    if not card or not ((FB_PAGE_ID and FB_TOKEN) or os.environ.get("CARDS_ALWAYS")):
        return ""
    for q in card.get("queries", []):  # find a free photo only now, when the card is really made
        if card.get("photo"):
            break
        card["photo"] = card_photo(commons_image(q)) if q else ""
    png = render_card(card)
    return send_card(png, "🖼 Facebook") if png else ""


def send_draft(s, url, text, stamp, image="", preview_url="", kind="news", note="", card=None, fb=""):
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
    if auto_publish_on(kind):
        at = (now() + timedelta(minutes=config.AUTO_PUBLISH_AFTER_MINUTES)).astimezone(LOCAL)
        note += "\n\n<i>⏱ " + config.LABELS["auto_publish_note"].format(time=f"{at:%H:%M}") + "</i>"
    msgs = []
    for admin in ADMIN_IDS:
        try:
            msg = tg("sendMessage", chat_id=admin, text=text + note, parse_mode="HTML",
                     link_preview_options=lp, reply_markup=buttons(did))
            msgs.append([admin_key(admin), msg["message_id"]])
        except Exception as e:  # e.g. this approver never pressed Start in the bot
            print(f"Could not send a draft to approver #{ADMIN_IDS.index(admin) + 1}: {e}")
    if msgs:
        s["pending"][did] = {"url": url, "text": text, "created": now().isoformat(), "msgs": msgs, "lp": lp,
                             "kind": kind}
        if fb:
            s["pending"][did]["fb"] = fb
        file_id = make_card(card)
        if file_id:
            s["pending"][did]["card"] = file_id
    return bool(msgs)


# ---------- referral lines in news ----------

def _ref_today(s):
    today = now().astimezone(LOCAL).strftime("%Y-%m-%d")
    r = s.get("ref_news", {})
    return r.get("count", 0) if r.get("date") == today else 0


def matching_referral(s, post):
    """A (text, link) offer that clearly fits this news story, within the daily limit; otherwise None."""
    refs = getattr(config, "REFERRALS", [])
    cap = getattr(config, "REFERRALS_IN_NEWS_PER_DAY", 0)
    waiting = sum(1 for d in s["pending"].values() if d.get("referral"))
    if not refs or _ref_today(s) + waiting >= cap:
        return None
    offers = "\n".join(f"[{i}] {r[0]} ({r[2] if len(r) > 2 else ''})" for i, r in enumerate(refs))
    pick = _json(ask_claude(REFERRAL_MATCH_PROMPT.format(
        offers=offers, post=f"{post['title']}\n{post['body']}"), schema=SCHEMA_REFERRAL), "{", "}") or {}
    try:
        i = int(pick.get("id"))
    except (TypeError, ValueError):
        return None
    if 0 <= i < len(refs):
        print(f"Referral added: {refs[i][0]}")
        return refs[i][:2]
    return None


# ---------- daily digest ----------

def visible_length(text):
    """Length of a Telegram HTML message as Telegram counts it: tags removed, entities decoded."""
    return len(html.unescape(re.sub(r"<[^>]+>", "", text)))


def outlet(source):
    """Media outlet from a feed name, e.g. "CBC Manitoba" -> "CBC" (prefixes in config.OUTLET_PREFIXES)."""
    for name in config.OUTLET_PREFIXES:
        if source.startswith(name):
            return name
    return source




def cmd_digest():
    if not ADMIN_IDS:
        sys.exit("TELEGRAM_ADMIN_ID is not set")
    s = load_state()
    s.setdefault("digest_regions", {})
    d = now().astimezone(LOCAL)
    items = [it for it in fetch_news({}, max_age_hours=36, limit=180) if it["region"] not in config.DIGEST_EXCLUDE_REGIONS]
    print(f"{len(items)} items for the digest")
    if len(items) < 5:
        return save_state(s)
    recent = sorted(s["digest_regions"], key=lambda r: s["digest_regions"][r], reverse=True)[:6]
    listing = "\n".join(
        f"[{i}] {'[UKRAINIAN COMMUNITY] ' if it.get('community') else ''}({it['region']}, {it['source']}, "
        f"{it['published'].astimezone(LOCAL).strftime('%a %b %d %H:%M') if it['published'] else '?'}) "
        f"{it['title']} — {it['summary'][:120]}" for i, it in enumerate(items))
    prompt = DIGEST_PROMPT.format(national=config.DIGEST_NATIONAL, regions=config.DIGEST_REGIONS,
                                  recent=", ".join(recent) or "none", items=listing, today=f"{d:%A, %B %d, %Y}")
    digest = _json(ask_claude(prompt, schema=SCHEMA_DIGEST), "{", "}")
    if not isinstance(digest, dict) or not digest.get("national"):
        sys.exit("Could not write the digest")
    edited = _json(ask_claude(EDIT_PROMPT.format(
        draft=json.dumps(digest, ensure_ascii=False), title="Daily news digest", summary="",
        article="\n".join(f"{it['title']} — {it['summary']}" for it in items)), schema=SCHEMA_DIGEST), "{", "}")
    if isinstance(edited, dict) and edited.get("national"):
        digest = edited

    e = html.escape

    used = {}  # line -> outlet

    def line(entry):
        try:
            it = items[int(entry["id"])]
        except (KeyError, ValueError, IndexError, TypeError):
            return ""
        text = entry.get("text", "")
        link = f'<a href="{e(it["url"], quote=True)}">'
        m = re.search(r"\[([^\]]+)\]", text)
        if not m:  # no marked phrase: link the first few words
            m = re.match(r"\s*((?:\S+\s+){0,3}\S+)", text)
        if not m:
            return ""
        before, phrase, after = text[:m.start()], m.group(1), text[m.end():].replace("[", "").replace("]", "")
        result = f"• {e(before, quote=False)}{link}{e(phrase, quote=False)}</a>{e(after, quote=False)}"
        used[result] = outlet(it["source"])
        return result

    y = d - timedelta(days=1)
    national = [l for l in map(line, digest["national"]) if l]
    regions = []
    for reg in digest.get("regions", []):
        lines = [l for l in map(line, reg.get("items", [])) if l]
        if lines:
            regions.append([reg, lines])
    community_lines = [l for l in map(line, digest.get("community") or []) if l]
    today_lines = [l for l in map(line, digest.get("today") or []) if l]

    def build():
        parts = [f"🗞 <b>{config.LABELS['digest_title']} · {y.day} {config.MONTHS[y.month - 1]}</b>", "",
                 f"<b>{config.LABELS['digest_national']}</b>"] + national
        for reg, lines in regions:
            parts += ["", f"📍 <b>{e(reg.get('region', ''), quote=False)}</b>"] + lines
        if community_lines:
            parts += ["", f"<b>{config.LABELS['digest_community']}</b>"] + community_lines
        if today_lines:
            parts += ["", f"📌 <b>{config.LABELS['digest_today']}, {d.day} {config.MONTHS[d.month - 1]}</b>"] + today_lines
        kept = national + [l for _, ls in regions for l in ls] + community_lines + today_lines
        outlets = list(dict.fromkeys(used[l] for l in kept if l in used))
        parts += ["", f"<i>{config.LABELS['digest_sources']}: {e(', '.join(outlets), quote=False)}</i>",
                  f"<a href=\"{config.TELEGRAPH_AUTHOR_URL}\">{e(config.TELEGRAPH_AUTHOR, quote=False)}</a>"]
        if referral:
            parts += ["", referral]
        return "\n".join(parts)

    refs = getattr(config, "REFERRALS", [])
    referral = ""
    if refs:  # one referral link per digest, rotating
        label, link = refs[s.get("ref_index", 0) % len(refs)][:2]
        s["ref_index"] = s.get("ref_index", 0) + 1
        referral = f"<a href=\"{e(link, quote=True)}\">{e(label, quote=False)}</a>"
        if config.REFERRAL_DISCLOSURE:
            referral += f"\n<i>{e(config.REFERRAL_DISCLOSURE, quote=False)}</i>"

    # Telegram counts only the visible text (max 4096). If too long, drop regional items from the end,
    # then whole regions, then extra national items - never the ending (sources, channel, referral).
    while visible_length(build()) > 4000:
        if regions and len(regions[-1][1]) > 1:
            regions[-1][1].pop()
        elif regions:
            regions.pop()
        elif len(national) > 3:
            national.pop()
        elif today_lines:
            today_lines.pop()
        elif community_lines:
            community_lines.pop()
        else:
            break
    text = build()
    for reg, _ in regions:
        s["digest_regions"][reg.get("region_en") or reg.get("region", "")] = d.strftime("%Y-%m-%d")
    try:
        top = items[int(digest["national"][0]["id"])]["url"]
    except (KeyError, ValueError, IndexError, TypeError):
        top = ""
    key = f"digest:{d:%Y-%m-%d}"
    n = config.CARD.get("digest_items", 4)
    heads = [re.sub(r"[\[\]]", "", x.get("text", "")).strip() for x in digest["national"][:n]]
    card = {"kind": "digest", "title": config.LABELS["digest_title"], "tag": f"{y.day} {config.MONTHS[y.month - 1]}",
            "items": [h if len(h) <= 110 else h[:107].rsplit(" ", 1)[0] + "…" for h in heads if h]}
    if send_draft(s, key, text, now().isoformat(), preview_url=top, kind="digest", card=card):
        print("Digest draft sent")
    save_state(s)


# ---------- Canadian history ----------
# Two daily columns, both approved like the news:
#   "📅 Цей день в історії Канади" (python bot.py thisday) - an event, birth or death on today's date
#   "🍁 Історія Канади"            (python bot.py history) - a story from the history sources in config.py


WIKI = f"https://{config.WIKIPEDIA_LANG}.wikipedia.org"
LOCAL = ZoneInfo(config.TIMEZONE)  # for picking "today", showing times and the schedule


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
        title = re.sub(r"_", " ", p.get("title", ""))
        tw = [w for w in re.findall(r"\w+", title.lower()) if len(w) > 2]
        hit = sum(w in words for w in tw) / len(tw) if tw else 0
        return (hit, len(tw))
    return max(pages, key=score).get("title", "")


def wiki_on_this_day(d):
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


_telegraph_session = {}


def telegraph(method, s, **params):
    """Call the Telegraph API (telegra.ph) with the account key from the TELEGRAPH_TOKEN secret.
    The key is never written to state.json (the repository may be public)."""
    if method not in ("createAccount", "revokeAccessToken"):
        token = TELEGRAPH_TOKEN or _telegraph_session.get("token")
        if not token:  # no secret yet: use a temporary account for this run
            print("TELEGRAPH_TOKEN is not set: using a temporary Telegraph account")
            acc = telegraph("createAccount", s, short_name=config.BOT_NAME[:32], author_name=config.TELEGRAPH_AUTHOR,
                            author_url=config.TELEGRAPH_AUTHOR_URL)
            token = _telegraph_session["token"] = acc["access_token"]
        params["access_token"] = token
    resp = json.loads(http(f"https://api.telegra.ph/{method}", params))
    if not resp.get("ok"):
        raise RuntimeError(f"Telegraph {method} failed: {resp.get('error')}")
    return resp["result"]


def telegraph_nodes(body, image, image_credit, source_name, url):
    """Turn the article text into Telegraph content: photo, paragraphs, subheadings, source."""
    nodes = []
    if image:
        nodes.append({"tag": "figure", "children": [{"tag": "img", "attrs": {"src": image}},
                                                    {"tag": "figcaption", "children": [f"{config.LABELS['photo']}: {image_credit}"]}]})
    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if block.startswith("#"):
            nodes.append({"tag": "h4", "children": [block.lstrip("# ").strip()]})
        elif block:
            nodes.append({"tag": "p", "children": [block]})
    nodes.append({"tag": "hr"})
    nodes.append({"tag": "p", "children": [config.LABELS["source"] + ": ", {"tag": "a", "attrs": {"href": url}, "children": [source_name]}]})
    nodes.append({"tag": "p", "children": [{"tag": "a", "attrs": {"href": config.TELEGRAPH_AUTHOR_URL},
                                            "children": [config.TELEGRAPH_AUTHOR]}]})
    return nodes


def history_card(kind, header, title, image, query, topic, credit=""):
    """Card for a history post: the post's photo if it's freely licensed, otherwise one from Wikimedia Commons."""
    tag = re.sub(r"^\W+", "", header).strip()  # the header without its emoji
    return {"kind": kind, "title": title, "tag": tag, "photo": card_photo(image), "credit": credit,
            "queries": [*split_queries(query), topic]}


def split_queries(query):
    """'A | B | C' -> ['A', 'B', 'C'] (the writer suggests several picture searches, best first)."""
    return [q.strip() for q in (query or "").split("|") if q.strip()][:4]


def fb_long(header, post, source_name):
    """The whole long-read as one Facebook post (Facebook readers may not open Telegram or Telegraph)."""
    body = re.sub(r"^##\s*(.+)$", lambda m: "▪️ " + m.group(1).strip().upper(), post["body"], flags=re.M)
    text = f"{header}\n\n{post['title'].upper()}\n\n{post['teaser']}\n\n{body}\n\n{config.LABELS['source']}: {source_name}"
    return fb_footer(text)


def _write_history(topic, source, article, opening, header, source_name, url, s, stamp, image=""):
    """Write a long-read, publish it on Telegraph, and send the teaser post as a draft."""
    kind = "thisday" if header == config.LABELS["thisday_header"] else "history"
    keys = ("title", "teaser", "body")
    post = write_long(HISTORY_WRITE_PROMPT.format(
        topic=topic, source=source_name, article=SOURCE_REF, opening=opening), keys, source=article,
        optional=("image_query",))
    if not post:
        print("Could not write the history post")
        return False
    query = (post.get("image_query") or "").strip()
    if not query and not image:  # ask separately: the English Wikipedia title of the main subject
        query = ask_claude("Give the exact English Wikipedia article title for the main person, place or event "
                           f"of this story: {topic}\nReply with the title only.").strip().strip('"')[:100]
    edited = parse_post(ask_claude(EDIT_PROMPT.format(
        draft=json.dumps({k: post[k] for k in keys}, ensure_ascii=False),
        title=topic, summary="", article=SOURCE_REF), source=article, schema=schema_post(keys)), keys)
    post = edited if edit_ok(post, edited) else post
    post, problems = review_post(post, keys, article, topic)
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
        return send_draft(s, url, text[:4000], stamp, image=image, kind=kind, note=review_note(problems),
                          card=history_card(kind, header, post["title"], image, query, topic, credit),
                          fb=fb_long(header, post, source_name))
    e = html.escape
    text = (f"{e(header, quote=False)}\n\n<b>{e(post['title'], quote=False)}</b>\n\n{e(post['teaser'], quote=False)}"
            f"\n\n📖 <b><a href=\"{e(page['url'], quote=True)}\">{e(config.LABELS['read_more'])} →</a></b>")
    # the source is credited at the end of the Telegraph article, not in the post
    print(f"Telegraph page: {page['url']}")
    ok = send_draft(s, url, text, stamp, preview_url=page["url"], kind=kind, note=review_note(problems),
                    card=history_card(kind, header, post["title"], image, query, topic, credit),
                    fb=fb_long(header, post, source_name))
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
            + (f".{year}" if year else "") + DATE_WORDS)


def cmd_thisday():
    """An event or a person on today's date, alternating day by day.
    People: config.PEOPLE_OF_THE_DAY. Events: Wikipedia "On this day", entries matching config.THISDAY_WORDS."""
    s = _history_state()
    stamp = now().isoformat()
    d = now().astimezone(LOCAL)
    header = config.LABELS["thisday_header"]
    want = "event" if s.get("thisday_last") != "event" else "person"

    cands = [{"kind": "person", "label": f"person (born or died on {d:%B} {d.day}): {b['name']}", **b}
             for b in people_of_the_day() if b["url"] not in s["history_done"]]
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
    for i in parse_picks(ask_claude(prompt, schema=SCHEMA_IDS))[:3]:
        if i >= len(cands):
            continue
        c = cands[i]
        if "wiki" in c:
            e = c["wiki"]
            _done(s, e["page"])
            article, url = wiki_text(e["page"])
            if len(article) < 500:
                continue
            ok = _write_history(f"{e['year']}: {e['text']}", config.LABELS["wikipedia"], article, _date_opening(d, e["year"]),
                                header, config.LABELS["wikipedia"], url, s, stamp, fetch_page(url)[1])
        else:
            _done(s, c["url"])
            article, image = fetch_page(c["url"], 15000)
            if len(article) < 800:
                continue
            ok = _write_history(f"{c['name']} (born or died on {d:%B} {d.day}; the text says which, and the year)",
                                config.PEOPLE_OF_THE_DAY["name"], article,
                                "Start with the date" + DATE_WORDS[:-1] + " and what happened on it: "
                                "the person's birth or death.",
                                header, config.PEOPLE_OF_THE_DAY["name"], c["url"], s, stamp, image)
        if ok:
            s["thisday_last"] = c["kind"]
            print(f"This-day draft sent ({c['kind']}): {c['label']}")
            break
    save_state(s)


def _story_from(candidates, s, stamp, header, community=False):
    """Let Claude rank the candidates, then write the first one that has enough text.
    On community days only stories mainly about the community count."""
    listing = "\n".join(f"[{i}] ({c['region']}, {c['source']}) {c['title']}" for i, c in enumerate(candidates))
    focus = COMMUNITY_FOCUS.format(community=config.COMMUNITY_HISTORY_LABEL) if community else ""
    for i in parse_picks(ask_claude(STORY_PICK_PROMPT.format(items=listing, focus=focus), schema=SCHEMA_IDS))[:3]:
        if i >= len(candidates):
            continue
        c = candidates[i]
        _done(s, c["url"])
        article, image = fetch_page(c["url"], 15000)
        if len(article) < 800:
            print(f"Too little text for {c['title']}; trying the next pick")
            continue
        key = getattr(config, "COMMUNITY_HISTORY_KEYWORD", "")
        if community and key and len(re.findall(key, article, re.I)) < 3:
            print(f"Not mainly about {config.COMMUNITY_HISTORY_LABEL}: {c['title']}; trying the next pick")
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
        if _write_history(title, config.LABELS["wikipedia"], article, "Open with a vivid detail or the key moment.",
                          header, config.LABELS["wikipedia"], url, s, stamp, image):
            print(f"History draft sent: {title} (Wikipedia fallback)")
            return True
    return False


def cmd_history(community=False):
    """Sources from config first; Wikipedia only if none of them gives a usable story."""
    s = _history_state()
    stamp = now().isoformat()
    header = config.LABELS["history_header"]
    if community or now().astimezone(LOCAL).weekday() == config.COMMUNITY_HISTORY_DAY:
        candidates = _collect(config.COMMUNITY_HISTORY_SOURCES, s, per_source=8)
        print(f"{len(candidates)} community-history candidates")
        ok = candidates and _story_from(candidates, s, stamp, header, community=True)
        if not ok:
            topics = [(config.COMMUNITY_HISTORY_LABEL, t) for t in config.COMMUNITY_HISTORY_TOPICS]
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
        telegraph("editPage", s, path=d["telegraph_path"], title=config.LABELS["unpublished"],
                  content=json.dumps([{"tag": "p", "children": [config.LABELS["unpublished"] + "."]}],
                                     ensure_ascii=False))
    except Exception as e:
        print(f"Could not retire Telegraph page: {e}")


def clean_link(url):
    """Remove tracking bits (config.STRIP_FROM_LINKS) from a link."""
    for part in config.STRIP_FROM_LINKS:
        url = url.replace(part, "")
    return url


def fb_footer(text):
    footer = getattr(config, "FB_FOOTER", "")
    return f"{text}\n\n{footer}" if footer else text


def fb_text(text):
    """Telegram HTML -> plain text for Facebook: links keep only their words (see FB_COMMENT for why),
    the channel signature and referral lines are dropped, and the FB_FOOTER line is added."""
    text = re.sub(r'<a href="[^"]*">&#8203;</a>', "", text)  # invisible image link
    drop = [config.TELEGRAPH_AUTHOR_URL]  # the digest's channel signature line
    if not getattr(config, "FB_REFERRALS", False):
        drop += [r[1] for r in getattr(config, "REFERRALS", [])]
    text = "\n".join(l for l in text.split("\n") if not any(f'href="{html.escape(u, quote=True)}"' in l for u in drop))
    text = re.sub(r'\n*📖 <b><a href="[^"]+">[^<]*</a></b>', "", text)  # "read more" (it goes in the comment)
    text = re.sub(r'<a href="[^"]+">(.*?)</a>', lambda m: re.sub(r"<[^>]+>", "", m.group(1)), text, flags=re.S)
    text = html.unescape(re.sub(r"</?(b|i|u|s)>", "", text))
    return fb_footer(re.sub(r"\n{3,}", "\n\n", text).strip())


def fb_comment(d):
    """The first comment: the clickable links Facebook allows (the channel, a Telegraph long-read)."""
    parts = []
    if d.get("lp", {}).get("url", "").startswith("https://telegra.ph/") and getattr(config, "FB_COMMENT_READ_MORE", ""):
        parts.append(config.FB_COMMENT_READ_MORE.format(url=d["lp"]["url"]))
    if getattr(config, "FB_COMMENT", ""):
        parts.append(config.FB_COMMENT)
    return "\n\n".join(parts)


def post_to_facebook(d):
    """Publish an approved post to the Facebook Page (only if the Facebook secrets are set): the picture card
    with the full text (or the text alone if there is no card), then the first comment with the links."""
    if not (FB_PAGE_ID and FB_TOKEN):
        return None
    message = d.get("fb") or fb_text(d["text"])
    api = "https://graph.facebook.com"
    if d.get("card"):
        path = tg("getFile", file_id=d["card"])["file_path"]
        png = http(f"https://api.telegram.org/file/bot{TG_TOKEN}/{path}")
        r = post_multipart(f"{api}/{FB_PAGE_ID}/photos", {"message": message, "access_token": FB_TOKEN},
                           {"source": ("card.png", png, "image/png")})
        post_id = r.get("post_id") or r.get("id")
    else:
        r = post_multipart(f"{api}/{FB_PAGE_ID}/feed", {"message": message, "access_token": FB_TOKEN}, {})
        post_id = r.get("id")
    comment = fb_comment(d)
    if comment and post_id:
        try:
            post_multipart(f"{api}/{post_id}/comments", {"message": comment, "access_token": FB_TOKEN}, {})
        except Exception as e:  # the post is out; a missing comment isn't worth failing over
            print(f"Facebook comment failed: {e}")
    return post_id or "ok"


def answer(cq, text, alert=False):
    # Telegram rejects answers to taps older than a few minutes; that's harmless.
    try:
        tg("answerCallbackQuery", callback_query_id=cq["id"], text=text, show_alert=alert)
    except Exception as e:
        print(f"(could not answer tap: {e})")


def publish_draft(d, s):
    """Post a draft to the channel (and Facebook). Returns a status suffix, or None if Telegram failed."""
    try:
        tg("sendMessage", chat_id=config.CHANNEL, text=d["text"], parse_mode="HTML",
           link_preview_options=d.get("lp") or preview(d["url"]))
    except Exception as e:
        print(f"PUBLISH ERROR: {e}")
        return None
    fb = ""
    try:
        if post_to_facebook(d):
            fb = " + Facebook"
    except Exception as e:
        print(f"FACEBOOK ERROR: {e}")
        fb = " (Facebook failed: check the token)"
    if d.get("referral"):
        today = now().astimezone(LOCAL).strftime("%Y-%m-%d")
        s["ref_news"] = {"date": today, "count": _ref_today(s) + 1}
    print(f"Published {d['url']}")
    return fb


def cmd_approve():
    s = load_state()
    updates = None
    for attempt in range(3):  # reading taps is safe to retry; a dropped connection is usually momentary
        try:
            updates = tg("getUpdates", offset=s["tg_offset"], timeout=0, allowed_updates=["callback_query"])
            break
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            print(f"Telegram unreachable ({e}); retrying" if attempt < 2 else
                  f"Telegram unreachable ({e}); taps will be read on the next run")
            if attempt < 2:
                import time
                time.sleep(5)
    if updates is None:
        return
    if updates:
        print(f"{len(updates)} update(s): " + ", ".join(k for u in updates for k in u if k != "update_id"))
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
            result = publish_draft(d, s)
            if result is None:
                answer(cq, "Publishing failed, check the bot is a channel admin", alert=True)
                continue
            answer(cq, "Published" + result)
            close_draft(d, f"✅ Published by {who}{result}")
        else:
            answer(cq, "Skipped")
            close_draft(d, f"❌ Skipped by {who}")
            retire_telegraph(d, s)
        del s["pending"][did]
        save_state(s)  # save after every tap so a later error can never cause a double post

    # Auto-publish: drafts of the kinds switched on in config.AUTO_PUBLISH go out after the waiting time
    due = (now() - timedelta(minutes=getattr(config, "AUTO_PUBLISH_AFTER_MINUTES", 60))).isoformat()
    for did, d in list(s["pending"].items()):
        if auto_publish_on(d.get("kind", "news")) and d["created"] < due:
            result = publish_draft(d, s)
            if result is not None:
                close_draft(d, f"✅ Published automatically{result}")
                del s["pending"][did]
                save_state(s)

    cutoff = (now() - timedelta(hours=config.DRAFT_EXPIRY_HOURS)).isoformat()
    for did, d in list(s["pending"].items()):
        if d["created"] < cutoff:
            close_draft(d, "⌛ Expired")
            retire_telegraph(d, s)
            del s["pending"][did]
    save_state(s)


def cmd_rewrite(path, source):
    """Rewrite an already published Telegraph long-read in place (same link) from a source:
    a web page URL, or "wiki:Article title" for English Wikipedia. Uses the current prompts and style guide."""
    s = load_state()
    if source.startswith("wiki:"):
        article, url = wiki_text(source[5:])
        image = fetch_page(url)[1] if url else ""
        source_name = config.LABELS["wikipedia"]
    else:
        article, image = fetch_page(source, 15000)
        url, source_name = source, urllib.parse.urlparse(source).netloc
    if len(article) < 500:
        sys.exit(f"Not enough text at {source}")
    keys = ("title", "teaser", "body")
    topic = source[5:] if source.startswith("wiki:") else source
    post = write_long(HISTORY_WRITE_PROMPT.format(
        topic=topic, source=source_name, article=SOURCE_REF, opening="Open with a vivid detail or the key moment."),
        keys, source=article, optional=("image_query",))
    if not post:
        sys.exit("Could not write the article")
    query = post.get("image_query", "")
    edited = parse_post(ask_claude(EDIT_PROMPT.format(
        draft=json.dumps({k: post[k] for k in keys}, ensure_ascii=False),
        title=topic, summary="", article=SOURCE_REF), source=article, schema=schema_post(keys)), keys)
    post = edited if edit_ok(post, edited) else post
    post, problems = review_post(post, keys, article, topic)
    if problems:
        print("Still flagged by the reviewer:", "; ".join(problems))
    credit = source_name
    if not image:
        image, credit = commons_image(query) or commons_image(topic), "Wikimedia Commons"
    print(f"Photo: {image or 'none found'}")
    page = telegraph("editPage", s, path=path, title=post["title"][:256], author_name=config.TELEGRAPH_AUTHOR,
                     author_url=config.TELEGRAPH_AUTHOR_URL,
                     content=json.dumps(telegraph_nodes(post["body"], image, credit, source_name, url),
                                        ensure_ascii=False))
    print(f"Rewritten: {page['url']}\nNew title: {post['title']}\nNew teaser (the channel post itself is unchanged): "
          f"{post['teaser']}")


def cmd_tick():
    """Runs every 5 minutes: starts the drafts that are due by config.SCHEDULE (local time, catching up on
    late runs), then publishes approved posts."""
    jobs = {"digest": cmd_digest, "thisday": cmd_thisday, "news": cmd_draft, "history": cmd_history}
    local = now().astimezone(LOCAL)
    for job, slots in config.SCHEDULE.items():
        for slot in slots:
            h, m = map(int, slot.split(":"))
            due = local.replace(hour=h, minute=m, second=0, microsecond=0)
            key = f"{job} {due:%Y-%m-%d %H:%M}"
            if not (due <= local < due + timedelta(hours=config.CATCH_UP_HOURS)):
                continue
            s = load_state()
            done = s.setdefault("schedule_done", {})
            if key in done:
                continue
            done[key] = now().isoformat()
            week_ago = (now() - timedelta(days=7)).isoformat()
            s["schedule_done"] = {k: v for k, v in done.items() if v > week_ago}
            save_state(s)  # mark first, so a crash can't make the same draft twice
            print(f"Running {key}")
            try:
                jobs[job]()
            except (Exception, SystemExit) as e:  # one job failing must not stop the others or publishing
                print(f"JOB ERROR {key}: {e}")
    cmd_approve()


def cmd_check():
    """Check the Telegram and Facebook connections without posting anything."""
    ok = True
    try:
        me, chat = tg("getMe"), tg("getChat", chat_id=config.CHANNEL)
        print(f"Telegram: OK, bot @{me['username']}, channel {chat.get('title')}")
        hook = tg("getWebhookInfo")
        if hook.get("url"):  # a webhook stops the bot from reading taps
            ok = False
            print(f"Telegram: a webhook is set ({hook['url'].split('/')[2]}); taps can't be read. Revoke the token.")
        print(f"Telegram: waiting taps {hook.get('pending_update_count', 0)}")
    except Exception as e:
        ok = False
        print(f"Telegram: FAILED ({e})")
    if not (FB_PAGE_ID and FB_TOKEN):
        print("Facebook: not set up (FACEBOOK_PAGE_ID / FACEBOOK_PAGE_TOKEN missing)")
    else:
        tok = urllib.parse.quote(FB_TOKEN)
        try:
            page = json.loads(http(f"https://graph.facebook.com/{FB_PAGE_ID}?fields=name&access_token={tok}"))
            info = json.loads(http(f"https://graph.facebook.com/debug_token?input_token={tok}&access_token={tok}"))["data"]
            exp = info.get("expires_at") or 0
            when = "never" if not exp else datetime.fromtimestamp(exp, timezone.utc).strftime("%Y-%m-%d")
            print(f"Facebook: OK, page {page.get('name')}, token type {info.get('type')}, expires {when}")
            print(f"Facebook permissions: {', '.join(info.get('scopes', []))}")
            if "pages_manage_posts" not in info.get("scopes", []):
                ok = False
                print(f"Facebook: the token can't post (missing pages_manage_posts; has {info.get('scopes')})")
        except Exception as e:
            ok = False
            print(f"Facebook: FAILED ({str(e).replace(FB_TOKEN, '***')})")
    if not ok:
        sys.exit(1)


def cmd_cards(path="samples/cards.json"):
    """Draw sample Facebook cards (to try changes to card.html): sends them to the approvers and saves them in cards/."""
    os.makedirs("cards", exist_ok=True)
    one = os.environ.get("CARD_JSON", "").strip()  # a single card given as JSON (e.g. for a post made earlier)
    cards = [json.loads(one)] if one else json.load(open(path, encoding="utf-8"))
    for i, card in enumerate(cards, 1):
        for q in card.get("queries", []):
            if not card.get("photo"):
                card["photo"] = card_photo(commons_image(q))
        png = render_card(card)
        if not png:
            continue
        name = f"cards/{i}-{card.get('kind', 'news')}.png"
        open(name, "wb").write(png)
        send_card(png, "🖼 Facebook" if one else f"🖼 Зразок картки: {card.get('kind', 'news')}")
        print(f"{name}: photo {card.get('photo') or 'none'}")


def cmd_edit(link):
    """Replace the text of a published channel post (Telegram only). Text from EDIT_TEXT: the first line is the
    headline, the rest the body. EDIT_SOURCE (optional): the source article link, added as the source line."""
    m = re.search(r"(\d+)\s*$", link.strip().rstrip("/"))
    text = os.environ.get("EDIT_TEXT", "").strip()
    if not m or not text:
        sys.exit("Usage: edit POST_LINK, with the new text in EDIT_TEXT")
    title, _, body = text.partition("\n")
    source = os.environ.get("EDIT_SOURCE", "").strip()
    if source:
        post = format_post(title.strip(), body.strip(), outlet_name(source), source)
    else:
        post = f"<b>{html.escape(title.strip(), quote=False)}</b>\n\n{html.escape(body.strip(), quote=False)}"
    tg("editMessageText", chat_id=config.CHANNEL, message_id=int(m.group(1)), text=post, parse_mode="HTML",
       link_preview_options=preview(source) if source else {"is_disabled": True})
    print(f"Edited post {m.group(1)}")


def outlet_name(url):
    """The display name of the feed this link comes from (e.g. Global News), or its domain."""
    host = urllib.parse.urlparse(url).netloc.replace("www.", "")
    for name, feed, _ in config.FEEDS:
        if urllib.parse.urlparse(feed).netloc.replace("www.", "") == host:
            return re.sub(r"\s+(Politics|BC|Calgary|Edmonton|Toronto|Winnipeg|Montreal|Halifax)$", "", name)
    return host


def cmd_post():
    """A draft from your own text (POST_TEXT: headline on the first line, then the body; POST_SOURCE: optional
    source link; POST_PHOTO: optional picture searches 'A | B'). It goes to the approvers like any draft,
    with its Facebook card, and is published to the channel and Facebook when approved."""
    text = os.environ.get("POST_TEXT", "").strip()
    if not text:
        sys.exit("POST_TEXT is empty")
    title, _, body = text.partition("\n")
    source = os.environ.get("POST_SOURCE", "").strip()
    s = load_state()
    if source:
        post = format_post(title.strip(), body.strip(), outlet_name(source), source)
        key = source
    else:
        post = f"<b>{html.escape(title.strip(), quote=False)}</b>\n\n{html.escape(body.strip(), quote=False)}"
        key = "own:" + hashlib.sha1(text.encode()).hexdigest()[:10]
    region = getattr(config, "REGIONS", {}).get("Canada", ("", ""))
    card = {"kind": "news", "title": title.strip(), "tag": region[0],
            "queries": [*split_queries(os.environ.get("POST_PHOTO", "")), region[1]]}
    if send_draft(s, key, post, now().isoformat(), card=card):
        print("Draft sent")
    save_state(s)


def cmd_recard(match):
    """Redraw the Facebook card of a waiting draft whose source link contains MATCH (e.g. after a design fix)."""
    s = load_state()
    for did, d in s["pending"].items():
        if match.lower() not in d["url"].lower():
            continue
        m = re.search(r"<b>(.*?)</b>", d["text"], re.S)
        title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))) if m else ""
        kind = d.get("kind") or "news"
        header = config.LABELS["thisday_header"] if kind == "thisday" else config.LABELS["history_header"]
        image = fetch_page(d["url"])[1] if d["url"].startswith("http") else ""
        card = (history_card(kind, header, title, image, "", "") if kind in ("history", "thisday")
                else {"kind": kind, "title": title})
        file_id = make_card(card)
        if file_id:
            d["card"] = file_id
            print(f"New card for: {title} (photo: {card.get('photo') or 'none'})")
    save_state(s)


def _print_usage():
    if _usage["calls"]:
        print(f"Claude usage: {_usage['calls']} calls, input {_usage['input']}, cache write {_usage['cache_write']}, "
              f"cache read {_usage['cache_read']}, output {_usage['output']} tokens")


if __name__ == "__main__":
    import atexit
    atexit.register(_print_usage)
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "draft":
        cmd_draft()
    elif cmd == "approve":
        cmd_approve()
    elif cmd == "history":
        cmd_history(community=len(sys.argv) > 2 and sys.argv[2] == "community")
    elif cmd == "thisday":
        cmd_thisday()
    elif cmd == "digest":
        cmd_digest()
    elif cmd == "tick":
        cmd_tick()
    elif cmd == "rewrite":  # rewrite TELEGRAPH_PATH SOURCE  (SOURCE = URL or "wiki:Title")
        cmd_rewrite(sys.argv[2], sys.argv[3])
    elif cmd == "cards":  # sample Facebook cards: cards [FILE]
        cmd_cards(*sys.argv[2:3])
    elif cmd == "edit":  # edit POST_LINK (text in EDIT_TEXT, source link in EDIT_SOURCE)
        cmd_edit(sys.argv[2] if len(sys.argv) > 2 else "")
    elif cmd == "post":  # a draft from your own text (POST_TEXT, POST_SOURCE, POST_PHOTO)
        cmd_post()
    elif cmd == "recard":  # recard MATCH: redraw a waiting draft's Facebook card
        cmd_recard(sys.argv[2] if len(sys.argv) > 2 else "")
    elif cmd == "check":  # test the connections, posts nothing
        cmd_check()
    elif cmd == "merge-state":  # used by save_state.sh: merge-state BASE OURS (theirs = state.json)
        with open(sys.argv[2], encoding="utf-8") as f:
            base = json.load(f)
        with open(sys.argv[3], encoding="utf-8") as f:
            ours = json.load(f)
        save_state(merge_state(base, ours, load_state()))
    else:
        sys.exit("Usage: python bot.py draft|approve|history|thisday|digest")
