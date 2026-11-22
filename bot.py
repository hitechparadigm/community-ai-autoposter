#!/usr/bin/env python3
"""Ukrainian Canada autoposter.

  python bot.py draft    - fetch news, have Claude pick and write posts (Ukrainian),
                           send drafts to you in Telegram with Publish / Skip buttons
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
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

import config

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(HERE, "state.json")
UA = "Mozilla/5.0 (compatible; UkrainianCanadaBot/1.0)"
ATOM = "{http://www.w3.org/2005/Atom}"
DC = "{http://purl.org/dc/elements/1.1/}"

TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ADMIN_ID = os.environ.get("TELEGRAM_ADMIN_ID", "").strip()
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
            got = parse_feed(http(url), name)
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

PROMPT = """You are the editor of "Ukrainian Canada", a Telegram channel for Ukrainians living in Canada \
(recent arrivals including CUAET, and the long-established community).

Below are fresh news items. Pick up to {n} that matter most to this audience, for example: immigration, \
status and permits, CUAET, government programs and benefits, cost of living, housing, jobs, \
Canada-Ukraine relations, Canadian support for Ukraine, Ukrainian community life in Canada, \
or major national news everyone in Canada is talking about. Skip routine crime, celebrity and sports stories. \
Never pick two items about the same story. Pick fewer, or none, if nothing is relevant.

For each pick, write a post in Ukrainian:
- "title": a short headline, at most 12 words
- "body": 2-4 sentences summarizing the news in your own words (never copy sentences from the source). \
If useful, add one sentence on why it matters for Ukrainians in Canada. Neutral, clear tone. \
Use only facts stated in the item; do not invent details.

Reply with JSON only, no other text:
[{{"id": <item id>, "title": "...", "body": "..."}}]

News items:
{items}
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


def parse_picks(text):
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        return []
    try:
        picks = json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return []
    return [p for p in picks if isinstance(p, dict) and {"id", "title", "body"} <= p.keys()]


# ---------- posts ----------

def format_post(title, body, source, url):
    e = html.escape
    return (f"<b>{e(title)}</b>\n\n{e(body)}\n\n"
            f"🔗 Джерело: <a href=\"{e(url, quote=True)}\">{e(source)}</a>")


def buttons(did):
    return {"inline_keyboard": [[
        {"text": "✅ Publish", "callback_data": f"pub:{did}"},
        {"text": "❌ Skip", "callback_data": f"skip:{did}"},
    ]]}


def preview(url):
    return {"url": url, "prefer_large_media": True}


def close_draft(d, status):
    """Replace the buttons on your draft message with a status line."""
    try:
        tg("editMessageText", chat_id=ADMIN_ID, message_id=d["admin_msg_id"],
           text=d["text"] + f"\n\n— {status}", parse_mode="HTML",
           link_preview_options={"is_disabled": True})
    except Exception as e:
        print(f"Could not update draft message: {e}")


# ---------- commands ----------

def cmd_draft():
    if not ADMIN_ID:
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
    picks = parse_picks(ask_claude(PROMPT.format(n=config.DRAFTS_PER_RUN, items=listing)))
    print(f"Claude picked {len(picks)}")

    stamp = now().isoformat()
    for it in items:  # don't offer the same stories again next run
        s["seen"][it["url"]] = stamp

    for p in picks[:config.DRAFTS_PER_RUN]:
        try:
            it = items[int(p["id"])]
        except (ValueError, IndexError):
            continue
        did = hashlib.sha1(it["url"].encode()).hexdigest()[:10]
        text = format_post(p["title"], p["body"], it["source"], it["url"])
        msg = tg("sendMessage", chat_id=ADMIN_ID, text=text, parse_mode="HTML",
                 link_preview_options=preview(it["url"]), reply_markup=buttons(did))
        s["pending"][did] = {"url": it["url"], "text": text, "created": stamp,
                             "admin_msg_id": msg["message_id"]}
        print(f"Draft sent: {it['title']}")
    save_state(s)


def cmd_approve():
    s = load_state()
    updates = tg("getUpdates", offset=s["tg_offset"], timeout=0,
                 allowed_updates=["callback_query"])
    for u in updates:
        s["tg_offset"] = u["update_id"] + 1
        cq = u.get("callback_query")
        if not cq:
            continue
        if str(cq["from"]["id"]) != ADMIN_ID:
            tg("answerCallbackQuery", callback_query_id=cq["id"], text="Not allowed")
            continue
        action, _, did = (cq.get("data") or "").partition(":")
        d = s["pending"].get(did)
        if not d:
            tg("answerCallbackQuery", callback_query_id=cq["id"], text="Already handled or expired")
            continue
        if action == "pub":
            try:
                tg("sendMessage", chat_id=config.CHANNEL, text=d["text"], parse_mode="HTML",
                   link_preview_options=preview(d["url"]))
            except Exception as e:
                print(f"PUBLISH ERROR: {e}")
                tg("answerCallbackQuery", callback_query_id=cq["id"],
                   text="Publishing failed, check the bot is a channel admin", show_alert=True)
                continue
            tg("answerCallbackQuery", callback_query_id=cq["id"], text="Published")
            close_draft(d, "✅ Published")
            print(f"Published {d['url']}")
        else:
            tg("answerCallbackQuery", callback_query_id=cq["id"], text="Skipped")
            close_draft(d, "❌ Skipped")
        del s["pending"][did]

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
    else:
        sys.exit("Usage: python bot.py draft|approve")
