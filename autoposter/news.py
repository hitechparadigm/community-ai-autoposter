"""News drafts (and the daily practical story) and the morning digest."""
import hashlib
import html
import json
import re
import sys
from datetime import timedelta

from community import config
from community.prompts import (DIGEST_PROMPT, DIGEST_SHORTLIST_PROMPT, EDIT_PROMPT, PICK_PROMPT, SHORTEN_TITLE,
                               TIPS_CHECK, TIPS_PICK_PROMPT, TIPS_WRITE_PROMPT, WRITE_PROMPT, REGION_FIELD)

from .core import ADMIN_IDS, LOCAL, load_state, now, save_state, visible_length
from .sources import fetch_article, fetch_news, outlet, split_queries
from .ai import SCHEMA_DIGEST, SCHEMA_IDS, SCHEMA_TIPS, SOURCE_REF, _json, ask_claude, edit_ok, parse_picks, parse_post, review_note, review_post, schema_post
from .channels import format_post
from .drafts import matching_referral, send_draft


def write_news(it, article, mode="news", idea=""):
    """Write, copy-edit and review one news (or "Варто знати") post from a story and its article text.
    Returns {"title", "body", "emoji", "photo_query", "problems"} (problems: what the reviewer still found),
    or None if Claude couldn't write it. Used for drafts and by the evaluation set (evals/)."""
    tips = mode == "tips"
    src_text = article or "(not available)"
    write_prompt = TIPS_WRITE_PROMPT if tips else WRITE_PROMPT
    summary = it["summary"] + (f"\nEDITOR'S REQUEST (follow it): {idea}" if idea else "")
    places = [r for r in getattr(config, "REGIONS", {}) if r not in config.COMMUNITY_REGIONS]
    where = REGION_FIELD.format(regions=", ".join(f'"{r}"' for r in places)) if places else ""
    post = parse_post(ask_claude(write_prompt.format(
        source=it["source"], title=it["title"], summary=summary, article=SOURCE_REF) + where, source=src_text,
        schema=schema_post(("title", "body"), ("image_query", "emoji", "tips", "region"))))
    if not post:
        print(f"Could not write post for: {it['title']}")
        return None
    photo_query = (post.pop("image_query", "") or "").strip()  # for the Facebook card
    region = (post.pop("region", "") or "").strip()  # where the story is about (the feed's region can differ)
    if region not in places:
        region = it["region"]
    emoji = (post.pop("emoji", "") or "").strip()[:4]  # shown before the headline
    advice = (post.pop("tips", "") or "").strip() if tips else ""  # general advice, checked on its own
    edited = parse_post(ask_claude(EDIT_PROMPT.format(
        draft=json.dumps(post, ensure_ascii=False), title=it["title"],
        summary=it["summary"], article=SOURCE_REF), source=src_text, schema=schema_post(("title", "body"))))
    if edit_ok(post, edited):
        post = edited
    else:
        print("Copy edit failed; using the first draft")
    limit = getattr(config, "TITLE_MAX_WORDS", 0)
    if limit and len(post["title"].split()) > limit:  # the writers sometimes run long: one short call to fix it
        short = ask_claude(SHORTEN_TITLE.format(words=limit, title=post["title"])).strip().strip("«»\"")
        if short and len(short.split()) <= limit:
            post["title"] = short
    post, problems = review_post(post, ("title", "body"), article or it["summary"], it["title"])
    if advice:  # general advice, not from the article: checked separately for accuracy and invented details
        checked = _json(ask_claude(TIPS_CHECK.format(story=post["body"], tips=advice), source=src_text,
                                   schema=SCHEMA_TIPS), "{", "}") or {}  # with the article: its own specifics stay
        if str(checked.get("tips", "")).count("•") >= 2:
            advice = checked["tips"].strip()
        post["body"] += f"\n\n{config.LABELS['tips_what_to_do']}\n{advice}"
    return {"title": post["title"], "body": post["body"], "emoji": emoji, "photo_query": photo_query,
            "region": region, "problems": problems}


def _draft_item(s, it, stamp, mode="news", idea=""):
    """Write one news (or "Варто знати") draft and send it to the approvers. idea: an approver's note to follow."""
    tips = mode == "tips"
    post = write_news(it, fetch_article(it["url"]), mode, idea)
    if not post:
        return False
    emoji, photo_query, problems = post["emoji"], post["photo_query"], post["problems"]
    header = config.LABELS["tips_header"] if tips else ""
    text = format_post(f"{emoji} {post['title']}".strip(), post["body"], it["source"], it["url"], header=header)
    ref = matching_referral(s, post)
    if ref:
        text += f'\n\n<a href="{html.escape(ref[1], quote=True)}">{html.escape(ref[0], quote=False)}</a>'
    where = post.get("region") or it["region"]
    region, fallback = getattr(config, "REGIONS", {}).get(where, (where, ""))
    community = it.get("community")
    card = {"kind": "community" if community else "news", "title": post["title"],
            "tag": (re.sub(r"^\W+", "", config.LABELS["tips_header"]).strip() if tips
                    else config.CARD.get("community_tag", region) if community else region),
            "queries": [*split_queries(photo_query), fallback]}
    if not send_draft(s, it["url"], text, stamp, note=review_note(problems), card=card, kind=mode):
        return False
    if ref:
        s["pending"][hashlib.sha1(it["url"].encode()).hexdigest()[:10]]["referral"] = True
    print(f"Draft sent: {it['title']}")
    return True


def cmd_draft(mode="news"):
    """News drafts. mode="tips": the daily practical story (consumer and family matters) with what to do."""
    tips = mode == "tips"
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
    pick_prompt = TIPS_PICK_PROMPT if tips else PICK_PROMPT
    picks = parse_picks(ask_claude(pick_prompt.format(n=config.DRAFTS_PER_RUN, items=listing), schema=SCHEMA_IDS,
                                   fast=True))
    print(f"Claude picked {picks}")

    stamp = now().isoformat()
    for it in items:  # don't offer the same stories again next run
        s["seen"][it["url"]] = stamp

    for i in picks[:config.DRAFTS_PER_RUN]:
        if i < len(items):
            _draft_item(s, items[i], stamp, mode)
    save_state(s)


def _digest_ids(digest, items):
    """The item ids the digest draft uses (the copy editor only needs those stories, not all of them)."""
    ids = set()
    for part in ("national", "community", "today"):
        ids |= {e.get("id") for e in digest.get(part, []) if isinstance(e, dict)}
    for reg in digest.get("regions", []):
        ids |= {e.get("id") for e in reg.get("items", []) if isinstance(e, dict)}
    return sorted(i for i in ids if isinstance(i, int) and 0 <= i < len(items))


def card_line(entry, limit=110):
    """A digest item for the picture card as a complete sentence: Claude's short version, else the item's first
    sentence if it fits, else the text cut at a word (with "…") as a last resort."""
    for h in (entry.get("short", ""), re.split(r"(?<=[.!?])\s+", entry.get("text", ""))[0]):
        h = re.sub(r"[\[\]]", "", h or "").strip()
        if h and len(h) <= limit:
            return h
    h = re.sub(r"[\[\]]", "", entry.get("text", "")).strip()
    return h if len(h) <= limit else h[:limit - 3].rsplit(" ", 1)[0] + "…"


def _shortlist(items):
    """Cut the day's items to the DIGEST_SHORTLIST most relevant, chosen by the cheaper FAST_MODEL from headlines
    only, so the digest writer (MODEL) reads a short list instead of every headline. Keeps the original order."""
    n = getattr(config, "DIGEST_SHORTLIST", 0)
    if not n or len(items) <= n:
        return items
    listing = "\n".join(f"[{i}] {'[UKRAINIAN COMMUNITY] ' if it.get('community') else ''}({it['region']}) "
                        f"{it['title']}" for i, it in enumerate(items))
    keep = set(parse_picks(ask_claude(DIGEST_SHORTLIST_PROMPT.format(n=n, items=listing), schema=SCHEMA_IDS,
                                      fast=True)))
    keep |= {i for i, it in enumerate(items) if it.get("community")}  # community news always goes through
    short = [it for i, it in enumerate(items) if i in keep]
    print(f"Shortlist: {len(short)} of {len(items)} items for the digest")
    return short if len(short) >= 20 else items  # a failed shortlist: use everything


def cmd_digest():
    """The morning digest: everything the feeds published since yesterday, grouped by Claude into national
    news, a few rotating regions, the community and today's events; each item links to its outlet."""
    if not ADMIN_IDS:
        sys.exit("TELEGRAM_ADMIN_ID is not set")
    s = load_state()
    s.setdefault("digest_regions", {})
    d = now().astimezone(LOCAL)
    # Everything the feeds published since yesterday 00:00 local time (straight from the outlets' feeds, not
    # from the channel), all items per feed, so a busy evening can't push yesterday's main stories out
    since = d.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    hours = (now() - since).total_seconds() / 3600
    items = [it for it in fetch_news({}, max_age_hours=hours, limit=config.DIGEST_MAX_ITEMS, per_feed=100)
             if it["region"] not in config.DIGEST_EXCLUDE_REGIONS]
    print(f"{len(items)} items for the digest")
    if len(items) < 5:
        return save_state(s)
    items = _shortlist(items)
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
        article="\n".join(f"[{i}] {items[i]['title']} — {items[i]['summary']}" for i in _digest_ids(digest, items))),
        schema=SCHEMA_DIGEST), "{", "}")
    if isinstance(edited, dict) and edited.get("national"):
        digest = edited

    e = html.escape

    used = {}  # line -> outlet

    def line(entry):
        """One digest item as a bullet whose [key phrase] links to the outlet's article."""
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
        """Assemble the digest text from the current lists (rebuilt while trimming to Telegram's length limit)."""
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
    card = {"kind": "digest", "title": config.LABELS["digest_title"], "tag": f"{y.day} {config.MONTHS[y.month - 1]}",
            "items": [h for h in map(card_line, digest["national"][:n]) if h]}
    if send_draft(s, key, text, now().isoformat(), preview_url=top, kind="digest", card=card):
        print("Digest draft sent")
    save_state(s)
