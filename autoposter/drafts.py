"""Drafts waiting for approval: sending them to approvers, daily counts, the learning log, publishing."""
import hashlib
import html
import re
from datetime import timedelta

from community import config
from community.prompts import REFERRAL_MATCH_PROMPT

from .core import ADMIN_IDS, LOCAL, admin_key, now, tg
from .ai import SCHEMA_REFERRAL, _json, ask_claude
from .cards import make_card
from .channels import buttons, post_to_facebook, preview


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


def auto_publish_on(kind):
    """Whether this kind of post goes out without approval (AUTO_PUBLISH in config.py)."""
    return bool(getattr(config, "AUTO_PUBLISH", {}).get(kind))


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
    note += "\n\n<i>" + html.escape(count_note(s, kind), quote=False) + "</i>"
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
        card_msgs = []
        file_id = make_card(card, card_msgs)
        if file_id:
            s["pending"][did]["card"] = file_id
            s["pending"][did]["card_msgs"] = card_msgs
            s["pending"][did]["card_spec"] = {k: v for k, v in card.items() if k != "queries"}
    return bool(msgs)


def _ref_today(s):
    """How many news posts with a referral link were published today."""
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
    pick = _json(ask_claude(fast=True, prompt=REFERRAL_MATCH_PROMPT.format(
        offers=offers, post=f"{post['title']}\n{post['body']}"), schema=SCHEMA_REFERRAL), "{", "}") or {}
    try:
        i = int(pick.get("id"))
    except (TypeError, ValueError):
        return None
    if 0 <= i < len(refs):
        print(f"Referral added: {refs[i][0]}")
        return refs[i][:2]
    return None


def publish_draft(d, s):
    """Post a draft to the channel (and Facebook). Returns a status suffix, or None if Telegram failed."""
    try:
        sent = tg("sendMessage", chat_id=config.CHANNEL, text=d["text"], parse_mode="HTML",
                  link_preview_options=d.get("lp") or preview(d["url"]))
    except Exception as e:
        print(f"PUBLISH ERROR: {e}")
        return None
    fb, fb_id = "", None
    try:
        fb_id = post_to_facebook(d)
        if fb_id:
            fb = " + Facebook"
    except Exception as e:
        print(f"FACEBOOK ERROR: {e}")
        fb = " (Facebook failed: check the token)"
    if d.get("referral"):
        today = now().astimezone(LOCAL).strftime("%Y-%m-%d")
        s["ref_news"] = {"date": today, "count": _ref_today(s) + 1}
    kind = d.get("kind") or "news"
    n, limit = daily_count(s, kind, add=1)
    learn(s, "published", d, tg=sent.get("message_id"), fb=fb_id if isinstance(fb_id, str) else None)
    print(f"Published {d['url']}")
    return fb + f" · {n}/{limit}" + (" ⚠️" if n > limit else "")


def daily_count(s, kind, add=0):
    """(published today, daily limit) for this kind of post; add=1 counts one more."""
    today = now().astimezone(LOCAL).strftime("%Y-%m-%d")
    log = s.setdefault("published_log", {})
    if add:
        log.setdefault(today, {})[kind] = log.get(today, {}).get(kind, 0) + add
        for day in [d for d in log if d < (now() - timedelta(days=60)).strftime("%Y-%m-%d")]:
            del log[day]
    limit = getattr(config, "DAILY_LIMITS", {}).get(kind) or len(config.SCHEDULE.get(kind, [])) or 1
    return log.get(today, {}).get(kind, 0), limit


def count_note(s, kind):
    """The draft's daily count line, e.g. "📊 Сьогодні опубліковано новин: 4 з 5" (⚠️ at or over the limit)."""
    n, limit = daily_count(s, kind)
    name = config.KIND_NAMES.get(kind, kind)
    over = " ⚠️" if n >= limit else ""
    return config.LABELS["count_line"].format(n=n, limit=limit, kind=name) + over


def learn(s, event, d=None, text="", **extra):
    """Remember what happened to a post (published, skipped, feedback, idea) for the monthly review."""
    m = re.search(r"<b>(.*?)</b>", (d or {}).get("text", ""), re.S)
    entry = {"t": now().isoformat(timespec="seconds"), "event": event, "kind": (d or {}).get("kind", ""),
             "title": html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))[:150] if m else "", "text": text[:500],
             **extra}
    cutoff = (now() - timedelta(days=120)).isoformat()
    s["learn"] = [e for e in s.get("learn", []) if e["t"] > cutoff][-1500:] + [entry]
