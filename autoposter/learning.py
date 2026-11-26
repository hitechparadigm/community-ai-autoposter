"""Learning from editors and readers: comments, reactions and the monthly review."""
import hashlib
import html
from datetime import timedelta

from community import config
from community.prompts import COMMENT_GIST_PROMPT, REVIEW_MONTH_PROMPT

from .core import ADMIN_IDS, FB_TOKEN, LOCAL, answer, load_state, now, save_state, tg
from .ai import SCHEMA_LESSONS, _json, ask_claude
from .channels import fb_stats


def record_comment(m, s):
    """A comment in the channel's discussion group, under one of our posts."""
    parent = m.get("reply_to_message") or {}
    origin = parent.get("forward_origin") or {}
    post_id = origin.get("message_id") if origin.get("type") == "channel" else None
    text = (m.get("text") or "").strip()
    if post_id and text:  # state.json is in a public repo: readers' words are kept only as a short, unsigned
        # gist of what they ask or say (no names, no quotes), written by Claude; emotional or off-topic ones not at all
        gist = ask_claude(COMMENT_GIST_PROMPT.format(comment=text[:600])).strip()
        if gist and gist.upper() != "SKIP":
            s["tg_comments"] = (s.get("tg_comments", []) + [{"post": post_id, "text": gist[:200],
                                                              "t": now().isoformat(timespec="seconds")}])[-800:]
        else:
            s["tg_comment_count"] = {**s.get("tg_comment_count", {}),
                                     str(post_id): s.get("tg_comment_count", {}).get(str(post_id), 0) + 1}


def cmd_review(force=False):
    """Monthly: what was published, skipped, rewritten and asked for, and how readers reacted. Claude writes a
    short report and proposes a few rules; approvers decide whether the rules guide future posts."""
    if not force and now().astimezone(LOCAL).day != getattr(config, "REVIEW_DAY", 1):
        return
    s = load_state()
    since = (now() - timedelta(days=30)).isoformat()
    events = [e for e in s.get("learn", []) if e["t"] > since]
    if len(events) < 10:
        print("Not enough history for a review yet")
        return save_state(s)
    comments_by_post = {}
    for c in s.get("tg_comments", []):
        if c["t"] > since:
            comments_by_post.setdefault(c["post"], []).append(c["text"])
    lines, comments = [], []
    for e in events:
        if e["event"] == "published":
            stats = fb_stats(e["fb"]) if e.get("fb") and FB_TOKEN else {}
            tg_r = sum(s.get("tg_reactions", {}).get(str(e.get("tg")), {}).values())
            lines.append(f"PUBLISHED {e['kind']}: {e['title']} | Telegram reactions {tg_r}, comments "
                         f"{len(comments_by_post.get(e.get('tg'), []))} | Facebook reactions "
                         f"{stats.get('reactions', '-')}, comments {stats.get('comments', '-')}, "
                         f"shares {stats.get('shares', '-')}")
            comments += [f"[{e['title'][:60]}] {t}" for t in
                         comments_by_post.get(e.get("tg"), []) + stats.get("comment_texts", [])]
        elif e["event"] == "skipped":
            lines.append(f"SKIPPED by editors {e['kind']}: {e['title']}")
        elif e["event"] == "feedback":
            lines.append(f"EDITOR FEEDBACK on {e['kind']} «{e['title']}»: {e['text']}")
        elif e["event"] == "idea":
            lines.append(f"EDITOR IDEA ({e.get('mode', '')}): {e['text']}")
    notes = "\n".join(f"- {n}" for n in s.get("editorial_notes", [])) or "(none yet)"
    r = _json(ask_claude(REVIEW_MONTH_PROMPT.format(events="\n".join(lines[:400]),
                                                    comments="\n".join(comments[:250]) or "(none)", notes=notes),
                         schema=SCHEMA_LESSONS), "{", "}") or {}
    report, lessons = str(r.get("report", "")).strip(), [str(x).strip() for x in r.get("lessons", []) if str(x).strip()]
    if not report:
        print("Review failed")
        return save_state(s)
    lid = hashlib.sha1(report.encode()).hexdigest()[:8]
    text = f"📈 <b>{config.LABELS['review_title']}</b>\n\n{html.escape(report, quote=False)}"
    markup = None
    if lessons:
        s.setdefault("lessons_pending", {})[lid] = lessons[:6]
        text += f"\n\n<b>{config.LABELS['review_rules']}</b>\n" + "\n".join(
            f"{i}. {html.escape(x, quote=False)}" for i, x in enumerate(lessons[:6], 1))
        markup = {"inline_keyboard": [[{"text": "✅ " + config.LABELS["review_accept"], "callback_data": f"lessons:{lid}:yes"},
                                       {"text": "❌ " + config.LABELS["review_reject"], "callback_data": f"lessons:{lid}:no"}]]}
    for admin in ADMIN_IDS:
        try:
            tg("sendMessage", chat_id=admin, text=text[:4096], parse_mode="HTML", reply_markup=markup)
        except Exception as e:
            print(f"Could not send the review: {e}")
    print("Review sent")
    save_state(s)


def handle_lessons(cq, s):
    """An approver tapped ✅/❌ under the monthly review: keep or drop the proposed rules."""
    _, lid, choice = (cq.get("data") or "::").split(":", 2)
    lessons = s.get("lessons_pending", {}).pop(lid, None)
    if lessons is None:
        return answer(cq, "Already handled")
    if choice == "yes":
        s["editorial_notes"] = (s.get("editorial_notes", []) + lessons)[-getattr(config, "MAX_EDITORIAL_NOTES", 30):]
        answer(cq, config.LABELS["review_saved"])
    else:
        answer(cq, config.LABELS["review_dropped"])
    try:
        tg("editMessageReplyMarkup", chat_id=cq["message"]["chat"]["id"], message_id=cq["message"]["message_id"],
           reply_markup={"inline_keyboard": []})
    except Exception:
        pass
    save_state(s)
