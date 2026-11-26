"""The approvers' side: button taps, replies with feedback, ideas and links sent to the bot."""
import html
import re
import urllib.error
import urllib.parse
from datetime import timedelta

from community import config
from community.prompts import DATE_WORDS, REVISE_PROMPT

from .core import ADMIN_IDS, admin_key, answer, load_state, now, save_state, tg, visible_length
from .sources import fetch_article, fetch_page, outlet_name, page_title, wiki_text
from .ai import SCHEMA_REVISED, SOURCE_REF, _json, ask_claude, fix_homoglyphs
from .channels import retire_telegraph
from .drafts import auto_publish_on, close_draft, learn, publish_draft, send_draft
from .news import _draft_item
from .history import _history_from, _write_history
from .research import research_topic
from .learning import handle_lessons, record_comment


# What Telegram sends the bot: taps, messages, approvers' reactions on drafts, readers' reaction counts
ALLOWED_UPDATES = ["callback_query", "message", "message_reaction", "message_reaction_count"]


def find_draft(s, sender, message_id):
    """The waiting draft whose message (the text or its Facebook card) this approver has as message_id."""
    key = admin_key(sender)
    return next(((k, v) for k, v in s["pending"].items()
                 if [key, message_id] in v.get("msgs", []) + v.get("card_msgs", [])), (None, None))


def decide(s, did, d, action, who):
    """Publish or skip a waiting draft (from a tap, a reply or a reaction). Returns the publish result text,
    "" for a skip, or None if publishing failed (the draft then stays waiting)."""
    if action == "pub":
        result = publish_draft(d, s)
        if result is None:
            return None
        close_draft(d, f"✅ Published by {who}{result}")
    else:
        result = ""
        close_draft(d, f"❌ Skipped by {who}")
        learn(s, "skipped", d)
        retire_telegraph(d, s)
    del s["pending"][did]
    save_state(s)  # save after every decision so a later error can never cause a double post
    return result


def _word(text):
    """A reply reduced to compare with PUBLISH_WORDS / SKIP_WORDS: lower case, no spaces or punctuation."""
    return re.sub(r"[\s.,!?:;\-—«»\"']+", "", text.lower())


def handle_reaction(r, s):
    """An approver put a reaction on a draft or its card: PUBLISH_REACTIONS (👍) publishes it."""
    sender = str((r.get("user") or {}).get("id", ""))
    if sender not in ADMIN_IDS:
        return
    new = {x.get("emoji") for x in r.get("new_reaction", [])} - {x.get("emoji") for x in r.get("old_reaction", [])}
    if not new & set(getattr(config, "PUBLISH_REACTIONS", ())):
        return
    did, d = find_draft(s, sender, r.get("message_id"))
    if d:
        who = html.escape(str(r["user"].get("first_name") or sender))
        print(f"Published by reaction: {d['url']}")
        if decide(s, did, d, "pub", who) is None:
            tg("sendMessage", chat_id=sender, text="Publishing failed, check the bot is a channel admin")


def handle_feedback(msg, s):
    """An approver replied to a draft: "publish"/"skip" (PUBLISH_WORDS, SKIP_WORDS) decides it; anything else is
    feedback, and the bot rewrites the draft and sends the new version for approval."""
    sender = str((msg.get("from") or {}).get("id", ""))
    reply = msg.get("reply_to_message") or {}
    feedback = (msg.get("text") or "").strip()
    if sender not in ADMIN_IDS or not feedback:
        return
    if not reply:
        handle_idea(msg, s, sender)
        return
    did, d = find_draft(s, sender, reply.get("message_id"))
    word = _word(feedback)
    action = ("pub" if word in map(_word, getattr(config, "PUBLISH_WORDS", ())) else
              "skip" if word in map(_word, getattr(config, "SKIP_WORDS", ())) else "")
    if d and action:
        who = html.escape(str(msg["from"].get("first_name") or sender))
        print(f"{'Published' if action == 'pub' else 'Skipped'} by reply: {d['url']}")
        if decide(s, did, d, action, who) is None:
            tg("sendMessage", chat_id=sender, text="Publishing failed, check the bot is a channel admin",
               reply_parameters={"message_id": msg["message_id"]})
        return
    if not d:
        tg("sendMessage", chat_id=sender, text=config.LABELS["feedback_gone"],
           reply_parameters={"message_id": msg["message_id"]})
        return
    tg("sendMessage", chat_id=sender, text=config.LABELS["feedback_working"],
       reply_parameters={"message_id": msg["message_id"]})
    print(f"Feedback on {d['url']}: {feedback[:200]}")
    learn(s, "feedback", d, feedback)
    who = html.escape(str(msg["from"].get("first_name") or sender))
    try:
        if d.get("topic"):  # a "Розбираємося" article: research and write it again with the feedback
            retire_telegraph(d, s)
            ok = research_topic(s, d["topic"], feedback)
        elif d.get("telegraph_path"):
            ok = _redo_long_read(d, feedback, s)
        else:
            ok = _revise_post(did, d, feedback, s)
    except Exception as e:
        print(f"FEEDBACK ERROR: {e}")
        ok = False
    if ok:
        close_draft(d, f"✏️ {config.LABELS['feedback_done']} ({who})")
    else:
        tg("sendMessage", chat_id=sender, text=config.LABELS["feedback_failed"],
           reply_parameters={"message_id": msg["message_id"]})


def handle_idea(msg, s, sender):
    """A message to the bot (not a reply): a link or an idea for a post. "історія …" / "/history …" makes a
    long-read, "варто знати …" / "/tips …" a practical story, a plain link a news post."""
    text = (msg.get("text") or "").strip()
    low = text.lower()
    say = lambda t: tg("sendMessage", chat_id=sender, text=t, reply_parameters={"message_id": msg["message_id"]})
    if low.startswith(("/start", "/help")) or not text:
        return say(config.LABELS["ideas_help"])
    mode = "news"
    for prefix, m in (("/history", "history"), ("/історія", "history"), ("історія", "history"),
                      ("/tips", "tips"), ("варто знати", "tips"), ("/news", "news")):
        if low.startswith(prefix):
            mode, text = m, text[len(prefix):].strip(" :—-")
            break
    urls = re.findall(r"https?://\S+", text)
    note = re.sub(r"https?://\S+", "", text).strip()
    if mode != "history" and not urls:  # a topic or a task, no link: search the web and write an article
        if len(note) < 15:
            return say(config.LABELS["idea_needs_link"])
        say(config.LABELS["research_working"])
        learn(s, "idea", None, msg.get("text", ""), mode="research")
        try:
            ok = research_topic(s, note)
        except Exception as e:
            print(f"RESEARCH ERROR: {e}")
            ok = False
        if not ok:
            say(config.LABELS["research_failed"])
        return
    say(config.LABELS["idea_working"])
    learn(s, "idea", None, msg.get("text", ""), mode=mode)
    ok = False
    try:
        if mode == "history":
            if urls:
                u = urls[0]
                src = ("wiki:" + urllib.parse.unquote(u.split("/wiki/", 1)[1])) if "wikipedia.org/wiki/" in u else u
            else:  # a topic: find its English Wikipedia article
                title = ask_claude("Give the exact English Wikipedia article title for this Canadian history topic: "
                                   f"{note}\nReply with the title only.").strip().strip('"«»')[:120]
                src = "wiki:" + title.replace(" ", "_")
            ok = _history_from(s, src, False, note)
        elif urls:
            u = urls[0]
            it = {"url": u, "title": page_title(u) or note or u, "summary": "", "source": outlet_name(u),
                  "region": "Canada", "published": now(),
                  "community": any(w in (note + " " + u) for w in config.COMMUNITY_WORDS)}
            s["seen"][u] = now().isoformat()
            ok = _draft_item(s, it, now().isoformat(), mode, idea=note)
    except Exception as e:
        print(f"IDEA ERROR: {e}")
    if not ok:
        say(config.LABELS["idea_failed"])


def _revise_post(did, d, feedback, s):
    """Rewrite a post (news, practical story, digest) by the feedback, keeping its links and format."""
    m = re.match(r'(<a href="[^"]*">&#8203;</a>)', d["text"])
    invisible = m.group(1) if m else ""
    text = d["text"][len(invisible):]
    source = fetch_article(d["url"]) if d["url"].startswith("http") else ""
    r = _json(ask_claude(REVISE_PROMPT.format(feedback=feedback, post=text,
                                              article=SOURCE_REF if source else "(not available)"),
                         source=source or None, schema=SCHEMA_REVISED), "{", "}") or {}
    new = fix_homoglyphs(str(r.get("text", "")).replace("\\n", "\n")).strip()
    links_before = set(re.findall(r'href="([^"]+)"', text))
    bad_tag = re.search(r"<(?!/?(b|i|u|s|a|code|blockquote)\b)[^>]*>", new)
    if (not new or bad_tag or visible_length(new) > 4000 or len(new) < 0.3 * len(text)
            or not set(re.findall(r'href="([^"]+)"', new)) <= links_before | set(re.findall(r'https?://\S+', feedback))):
        print("Revision rejected (empty, broken HTML, too long or new links)")
        return False
    old = dict(d)
    card = dict(d.get("card_spec") or {})
    m = re.search(r"<b>(.*?)</b>", new, re.S)
    if card and m:  # new headline on the Facebook card
        card["title"] = re.sub(r"^\W+\s*", "", html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip()
    image = html.unescape(re.search(r'href="([^"]*)"', invisible).group(1)) if invisible else ""
    lp_url = (d.get("lp") or {}).get("url", "")
    sent = send_draft(s, d["url"], new, d["created"], kind=d.get("kind", "news"), card=card or None, image=image,
                      preview_url=lp_url if lp_url and lp_url != d["url"] and not image else "")
    if sent:
        for k in ("referral",):  # keep what the old draft had
            if old.get(k):
                s["pending"][did][k] = old[k]
    return sent


def _redo_long_read(d, feedback, s):
    """Write a long-read (history, this day) again from its source, following the feedback."""
    url = d["url"]
    if "wikipedia.org/wiki/" in url:
        article, url = wiki_text(urllib.parse.unquote(url.split("/wiki/", 1)[1]))
        image, source_name = fetch_page(url)[1], config.LABELS["wikipedia"]
    else:
        article, image = fetch_page(url, 15000)
        source_name = urllib.parse.urlparse(url).netloc.replace("www.", "")
    if len(article) < 500:
        return False
    m = re.search(r"<b>(.*?)</b>", d["text"], re.S)
    title = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))) if m else url
    kind = d.get("kind") or "history"
    header = config.LABELS["thisday_header" if kind == "thisday" else "history_header"]
    opening = ("Start with the date" + DATE_WORDS[:-1] + " and what happened on it." if kind == "thisday"
               else "Open with a vivid detail or the key moment.")
    opening += (f"\n\nEDITOR'S FEEDBACK on the previous version (titled «{title}»); follow it closely: {feedback}")
    retire_telegraph(d, s)
    return _write_history(title, source_name, article, opening, header, source_name, d["url"], s,
                          now().isoformat(), image)


def cmd_approve():
    """Every run: read Telegram updates (taps, replies, ideas, comments, reactions) and act on them,
    publish drafts due for auto-publishing, and expire drafts older than DRAFT_EXPIRY_HOURS."""
    s = load_state()
    updates = None
    for attempt in range(3):  # reading taps is safe to retry; a dropped connection is usually momentary
        try:
            updates = tg("getUpdates", offset=s["tg_offset"], timeout=0, allowed_updates=ALLOWED_UPDATES)
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
        print(f"{len(updates)} update(s) from {s['tg_offset']}: " + ", ".join(
            f"{u['update_id']} " + "/".join(k for k in u if k != "update_id") for u in updates))
        # Tell Telegram right away that these taps are handled. Otherwise a run that started from an older copy
        # of state.json (another tick, or a manual run) would get the same taps again and post twice.
        try:
            tg("getUpdates", offset=updates[-1]["update_id"] + 1, timeout=0, limit=1, allowed_updates=ALLOWED_UPDATES)
        except Exception as e:
            print(f"(could not confirm the taps: {e})")
    for u in updates:
        s["tg_offset"] = u["update_id"] + 1
        if u.get("message_reaction_count"):  # readers' reactions to a channel post (anonymous counts)
            r = u["message_reaction_count"]
            s.setdefault("tg_reactions", {})[str(r["message_id"])] = {
                (x["type"].get("emoji") or x["type"].get("type", "?")): x["total_count"] for x in r.get("reactions", [])}
            continue
        if u.get("message_reaction"):  # an approver's reaction on a draft (👍 = publish)
            handle_reaction(u["message_reaction"], s)
            continue
        if u.get("message"):
            m = u["message"]
            if m.get("chat", {}).get("type") in ("group", "supergroup"):  # a reader's comment under a post
                record_comment(m, s)
            else:  # an approver's message: a reply to a draft = feedback; anything else = an idea for a post
                handle_feedback(m, s)
                save_state(s)
            continue
        cq = u.get("callback_query")
        if not cq:
            continue
        if (cq.get("data") or "").startswith("lessons:"):
            if str(cq["from"]["id"]) in ADMIN_IDS:
                handle_lessons(cq, s)
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
        result = decide(s, did, d, "pub" if action == "pub" else "skip", who)
        if result is None:
            answer(cq, "Publishing failed, check the bot is a channel admin", alert=True)
        else:
            answer(cq, "Published" + result if action == "pub" else "Skipped")

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
