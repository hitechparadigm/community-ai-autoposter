#!/usr/bin/env python3
"""Ukrainian Canada autoposter.

  python bot.py draft    - fetch news, have Claude pick and write posts (Ukrainian),
                           send drafts to you in Telegram with Publish / Skip buttons
  python bot.py history  - draft one "Canadian history" story
  python bot.py approve  - check your button taps and publish approved posts to the channel

No third-party packages needed (standard library only).
"""
import hashlib
import html
import json
import os
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
- People: full Ukrainian transliteration of the name plus their role on first mention \
(e.g. міністерка промисловості Канади Мелані Жолі). Use feminine job titles for women.
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


def fetch_article(url, limit=6000):
    """Best-effort plain text of a news article (paragraph text only)."""
    try:
        page = http(url, timeout=20).decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Could not fetch article: {e}")
        return ""
    page = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", page)
    paras = [_clean(p, 2000) for p in re.findall(r"(?is)<p[^>]*>(.*?)</p>", page)]
    text = "\n".join(p for p in paras if len(p) > 60)
    return text[:limit]


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


def send_draft(s, url, text, stamp):
    """Send a draft with Publish/Skip buttons to every approver and remember it."""
    did = hashlib.sha1(url.encode()).hexdigest()[:10]
    msgs = []
    for admin in ADMIN_IDS:
        try:
            msg = tg("sendMessage", chat_id=admin, text=text, parse_mode="HTML",
                     link_preview_options=preview(url), reply_markup=buttons(did))
            msgs.append([admin, msg["message_id"]])
        except Exception as e:  # e.g. this approver never pressed Start in the bot
            print(f"Could not send draft to {admin}: {e}")
    if msgs:
        s["pending"][did] = {"url": url, "text": text, "created": stamp, "msgs": msgs}
    return bool(msgs)


# ---------- Canadian history ----------

CANADA_WORDS = ("Canad", "Quebec", "Québec", "Ontario", "Manitoba", "Saskatchewan", "Alberta",
                "British Columbia", "Nova Scotia", "New Brunswick", "Newfoundland", "Labrador",
                "Prince Edward Island", "Yukon", "Nunavut", "Northwest Territories", "Toronto",
                "Montreal", "Montréal", "Vancouver", "Winnipeg", "Ottawa", "Halifax", "Calgary",
                "Edmonton", "Regina", "Saskatoon", "Hudson's Bay", "Klondike", "Mountie")

HISTORY_PICK_PROMPT = AUDIENCE + """

For a daily "Canadian history" column, pick the ONE most interesting story from these \
"on this day" entries. Prefer stories with a human angle, surprising facts, or a connection to \
immigrants or Ukrainians in Canada. Avoid dry administrative events and anything gruesome.

Reply with JSON only: [<entry id>] (or [] if none is interesting)

Entries:
{items}
"""

HISTORY_WRITE_PROMPT = AUDIENCE + "\n\n" + STYLE + """

Write a "Canadian history" post in Ukrainian based on the encyclopedia article below. \
It should read like a good magazine column: engaging, but strictly accurate.

- "title": a short, intriguing headline, at most 12 words (no clickbait, no exclamation marks)
- "body": 3-4 short paragraphs (about 900-1400 characters in total), separated by blank lines. \
Open with a vivid detail or the key moment{date_hint}, then tell the story, then why it matters \
or what it left behind. Mention a connection to Ukrainians in Canada only if the article supports it.
- Write in your own words. Use only facts stated in the article; do not invent dialogue, details or numbers.

Reply with JSON only: {{"title": "...", "body": "..."}}

Topic: {topic}
Article:
{article}
"""


def wiki_text(title, limit=7000):
    """Plain-text article from English Wikipedia (empty string if missing)."""
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


def on_this_day():
    d = now().astimezone(timezone(timedelta(hours=-5)))
    raw = http(f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/{d:%m}/{d:%d}")
    data = json.loads(raw)
    entries = []
    for kind in ("selected", "events", "births", "deaths"):
        for e in data.get(kind, []):
            pages = e.get("pages") or []
            blob = e.get("text", "") + " " + " ".join(p.get("extract", "") for p in pages[:2])
            if pages and any(w in blob for w in CANADA_WORDS):
                entries.append({"kind": kind, "year": e.get("year"), "text": e.get("text", ""),
                                "page": pages[0].get("title", "")})
    return entries, d


def cmd_history():
    if not ADMIN_IDS:
        sys.exit("TELEGRAM_ADMIN_ID is not set")
    s = load_state()
    s.setdefault("history_done", [])
    stamp = now().isoformat()
    topic = page = date_hint = ""

    today = now().astimezone(timezone(timedelta(hours=-5)))
    use_ukrainian = today.weekday() == config.UKRAINIAN_CANADIAN_DAY
    if not use_ukrainian:
        try:
            entries, d = on_this_day()
        except Exception as e:
            print(f"On-this-day error: {e}")
            entries = []
        entries = [e for e in entries if e["page"] not in s["history_done"]]
        print(f"{len(entries)} Canada-related on-this-day entries")
        if entries:
            listing = "\n".join(f"[{i}] {e['year']} ({e['kind']}): {e['text']}"
                                for i, e in enumerate(entries[:40]))
            picks = parse_picks(ask_claude(HISTORY_PICK_PROMPT.format(items=listing)))
            if picks and picks[0] < len(entries):
                e = entries[picks[0]]
                page = e["page"]
                topic = f"{e['year']}: {e['text']}"
                date_hint = f" (this happened on this day, {d.day}.{d.month}.{e['year']})"
    if not page:  # Ukrainian-Canadian day, or nothing good today
        left = [t for t in config.UKRAINIAN_CANADIAN_TOPICS if t not in s["history_done"]]
        if not left:
            s["history_done"] = [t for t in s["history_done"]
                                 if t not in config.UKRAINIAN_CANADIAN_TOPICS]
            left = list(config.UKRAINIAN_CANADIAN_TOPICS)
        page = topic = left[0]

    article, url = wiki_text(page)
    if not article:
        print(f"No article for {page}; skipping")
        s["history_done"].append(page)
        save_state(s)
        return
    post = parse_post(ask_claude(HISTORY_WRITE_PROMPT.format(
        topic=topic, article=article, date_hint=date_hint)))
    if not post:
        sys.exit("Could not write the history post")
    edited = parse_post(ask_claude(EDIT_PROMPT.format(
        draft=json.dumps(post, ensure_ascii=False), title=topic, summary="", article=article)))
    post = edited or post
    text = format_post(post["title"], post["body"], "Вікіпедія", url, header="🍁 Історія Канади")
    if send_draft(s, url, text, stamp):
        print(f"History draft sent: {page}")
    s["history_done"].append(page)
    s["history_done"] = s["history_done"][-500:]
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
                   link_preview_options=preview(d["url"]))
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
        cmd_history()
    else:
        sys.exit("Usage: python bot.py draft|approve|history")
