"""Canadian history: "this day in history" and long-reads published on Telegraph."""
import hashlib
import html
import json
import random
import re
import sys
import urllib.parse

from community import config
from community.prompts import (COMMUNITY_FOCUS, DATE_WORDS, EDIT_PROMPT, HISTORY_WRITE_PROMPT, STORY_PICK_PROMPT,
                     THISDAY_PICK_PROMPT)

from .core import ADMIN_IDS, LOCAL, load_state, now, save_state
from .sources import commons_image, fetch_page, harvest, people_of_the_day, split_queries, wiki_on_this_day, wiki_text
from .ai import SCHEMA_IDS, SOURCE_REF, ask_claude, edit_ok, parse_picks, parse_post, review_note, review_post, schema_post, write_long
from .cards import card_photo
from .channels import fb_long, format_post, telegraph, telegraph_nodes
from .drafts import send_draft


def history_card(kind, header, title, image, query, topic, credit=""):
    """Card for a history post: the post's photo if it's freely licensed, otherwise one from Wikimedia Commons."""
    tag = re.sub(r"^\W+", "", header).strip()  # the header without its emoji
    return {"kind": kind, "title": title, "tag": tag, "photo": card_photo(image), "credit": credit,
            "queries": [*split_queries(query), topic]}


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
    """The bot's memory, with the list of history sources already used."""
    if not ADMIN_IDS:
        sys.exit("TELEGRAM_ADMIN_ID is not set")
    s = load_state()
    s.setdefault("history_done", [])
    return s


def _done(s, key):
    """Remember that this history source was used (the last 1000 are kept)."""
    s["history_done"].append(key)
    s["history_done"] = s["history_done"][-1000:]


def _date_opening(d, year=""):
    """The writer's instruction to open a this-day post with the date."""
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
    """Candidate history stories: a few unused article links from each source's index pages."""
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


def cmd_history_from(source, thisday=False):
    """A history (or this-day) draft from a source you choose: a web page, or "wiki:Article_title"."""
    s = _history_state()
    _history_from(s, source, thisday)
    save_state(s)


def _history_from(s, source, thisday=False, idea=""):
    """Write a history (or this-day) draft from one source, optionally following an approver's request."""
    if source.startswith("wiki:"):
        article, url = wiki_text(source[5:])
        image = fetch_page(url)[1] if url else ""
        source_name = config.LABELS["wikipedia"]
    else:
        article, image = fetch_page(source, 15000)
        url, source_name = source, urllib.parse.urlparse(source).netloc.replace("www.", "")
    if len(article) < 500:
        print(f"Not enough text at {source}")
        return False
    topic = source[5:].replace("_", " ") if source.startswith("wiki:") else source
    d = now().astimezone(LOCAL)
    header = config.LABELS["thisday_header" if thisday else "history_header"]
    opening = ("Start with the date" + DATE_WORDS[:-1] + " and what happened on it." if thisday
               else "Open with a vivid detail or the key moment.")
    if idea:
        opening += f"\n\nEDITOR'S REQUEST (follow it): {idea}"
    ok = _write_history(f"{topic} ({d:%B} {d.day})" if thisday else topic, source_name, article, opening, header,
                        source_name, url, s, now().isoformat(), image)
    if ok:
        print(f"Draft sent: {topic}")
    return ok
