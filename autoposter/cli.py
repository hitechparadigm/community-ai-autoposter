"""Commands that tie the rest together: the 5-minute tick, checks, previews, manual tools."""
import hashlib
import html
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone

from community import config

from .core import FB_PAGE_ID, FB_TOKEN, LOCAL, http, load_state, merge_state, now, save_state, tg
from .ai import _print_usage
from .sources import commons_image, fetch_page, outlet_name, parse_feed, split_queries
from .cards import card_photo, make_card, render_card, send_card
from .channels import format_post, preview
from .drafts import send_draft
from .news import cmd_digest, cmd_draft
from .history import cmd_history, cmd_history_from, cmd_rewrite, cmd_thisday, history_card
from .learning import cmd_review, cmd_stats
from .evals import cmd_eval
from .research import NotCovered, research_topic
from .approval import cmd_approve


def cmd_tick():
    """Runs every 5 minutes: starts the drafts that are due by config.SCHEDULE (local time, catching up on
    late runs), then publishes approved posts."""
    jobs = {"digest": cmd_digest, "thisday": cmd_thisday, "news": cmd_draft, "history": cmd_history,
            "tips": lambda: cmd_draft("tips"), "review": cmd_review}
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
        if hook.get("pending_update_count"):  # peek (doesn't mark anything as read)
            peek = tg("getUpdates", timeout=0, limit=10)
            print("Telegram: waiting updates " + ", ".join(
                f"{u['update_id']}:{'/'.join(k for k in u if k != 'update_id')}" for u in peek)
                  + f"; the bot reads from {load_state().get('tg_offset')}")
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
            feed = json.loads(http(f"https://graph.facebook.com/{FB_PAGE_ID}/posts?fields=created_time,message"
                                   f"&limit=3&access_token={tok}")).get("data", [])
            for p in feed:  # the latest posts, to confirm what went out
                print(f"Facebook latest: {p.get('created_time')} {(p.get('message') or '')[:60]!r}")
            if "pages_manage_posts" not in info.get("scopes", []):
                ok = False
                print(f"Facebook: the token can't post (missing pages_manage_posts; has {info.get('scopes')})")
        except Exception as e:
            ok = False
            print(f"Facebook: FAILED ({str(e).replace(FB_TOKEN, '***')})")
    feeds = list(config.FEEDS) + [tuple(f.split("|", 1)) + ("test",) for f in os.environ.get("TEST_FEEDS", "").split()]
    broken = []
    for name, url, _region in feeds:  # every news feed should give stories
        try:
            n = len(parse_feed(http(url, timeout=45), name))
        except Exception as e:
            n, name = 0, f"{name} ({str(e)[:80]})"
        if not n and not name.startswith("News search"):  # a search can simply have no results today
            broken.append(name)
        elif _region == "test":
            print(f"Feed test OK: {name} — {n} stories")
    print(f"Feeds: {len(feeds) - len(broken)} of {len(feeds)} working" + (f"; not working: {'; '.join(broken)}" if broken else ""))
    if not ok:
        sys.exit(1)


def cmd_cards(path="community/samples/cards.json"):
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
        if d.get("card_spec"):  # the card as first made (kind, title, tag, date): redraw it, finding a photo again
            card = {k: v for k, v in d["card_spec"].items() if k not in ("photo", "credit")}
            card["queries"] = [title] if kind in ("history", "thisday") else []
        else:
            card = (history_card(kind, header, title, image, "", "") if kind in ("history", "thisday")
                    else {"kind": kind, "title": title})
        sent = []
        file_id = make_card(card, sent)
        if file_id:
            d["card"], d["card_msgs"] = file_id, d.get("card_msgs", []) + sent
            d["card_spec"] = {k: v for k, v in card.items() if k != "queries"}
            print(f"New card for: {title} (photo: {card.get('photo') or 'none'})")
    save_state(s)


def main(argv=None):
    """python bot.py COMMAND [ARGS]: see bot.py for the list."""
    import atexit
    atexit.register(_print_usage)
    argv = sys.argv if argv is None else argv
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "draft":
        cmd_draft(argv[2] if len(argv) > 2 else "news")  # draft [tips]
    elif cmd == "approve":
        cmd_approve()
    elif cmd == "history":
        cmd_history(community=len(argv) > 2 and argv[2] == "community")
    elif cmd == "thisday":
        cmd_thisday()
    elif cmd == "digest":
        cmd_digest()
    elif cmd == "tick":
        cmd_tick()
    elif cmd == "rewrite":  # rewrite TELEGRAPH_PATH SOURCE  (SOURCE = URL or "wiki:Title")
        cmd_rewrite(argv[2], argv[3])
    elif cmd == "cards":  # sample Facebook cards: cards [FILE]
        cmd_cards(*argv[2:3])
    elif cmd == "edit":  # edit POST_LINK (text in EDIT_TEXT, source link in EDIT_SOURCE)
        cmd_edit(argv[2] if len(argv) > 2 else "")
    elif cmd == "post":  # a draft from your own text (POST_TEXT, POST_SOURCE, POST_PHOTO)
        cmd_post()
    elif cmd == "recard":  # recard MATCH: redraw a waiting draft's Facebook card
        cmd_recard(argv[2] if len(argv) > 2 else "")
    elif cmd == "history-from":  # history-from SOURCE [thisday]
        cmd_history_from(argv[2], len(argv) > 3 and argv[3] == "thisday")
    elif cmd == "review":  # the monthly review now (normally on REVIEW_DAY)
        cmd_review(force=True)
    elif cmd == "research":  # an article on a topic (TOPIC), like a topic sent to the bot without a link
        topic = os.environ.get("TOPIC", "").strip() or " ".join(argv[2:])
        s = load_state()
        try:
            ok = research_topic(s, topic)
        except NotCovered as e:
            sys.exit(f"The sources found don't cover the topic: {e}")
        save_state(s)
        if not ok:
            sys.exit("Could not write the article")
    elif cmd == "eval":  # eval [CASE_ID ...]: the evaluation set (evals/)
        cmd_eval(argv[2:])
    elif cmd == "stats":  # stats [DAYS]: production numbers into docs/RESULTS.md
        cmd_stats(int(argv[2]) if len(argv) > 2 else 30)
    elif cmd == "check":  # test the connections, posts nothing
        cmd_check()
    elif cmd == "merge-state":  # used by save_state.sh: merge-state BASE OURS (theirs = state.json)
        with open(argv[2], encoding="utf-8") as f:
            base = json.load(f)
        with open(argv[3], encoding="utf-8") as f:
            ours = json.load(f)
        save_state(merge_state(base, ours, load_state()))
    else:
        sys.exit("Usage: python bot.py tick|draft [tips]|digest|thisday|history [community]|history-from SOURCE [thisday]|"
                 "approve|research TOPIC|review|eval [ID]|stats [DAYS]|rewrite PAGE SOURCE|post|edit LINK|recard MATCH|cards [FILE]|check|merge-state BASE OURS")
