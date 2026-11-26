"""Articles on a topic an approver sends without a link ("🔎 Розбираємося"): the bot searches the web, picks the
most reliable pages, reads them, and writes a long-read from them (published on Telegraph, with a teaser post
and the list of sources), checked by the same copy editor and reviewer as every other post."""
import hashlib
import html
import json
import urllib.parse

from community import config
from community.prompts import EDIT_PROMPT, RESEARCH_PICK_PROMPT, RESEARCH_QUERIES_PROMPT, RESEARCH_WRITE_PROMPT

from .core import now
from .sources import commons_image, fetch_article, split_queries, web_search
from .ai import (SCHEMA_IDS, SOURCE_REF, _json, ask_claude, edit_ok, parse_picks, parse_post, review_note,
                 review_post, schema_post, write_long)
from .channels import fb_long, telegraph, telegraph_nodes
from .drafts import send_draft

SCHEMA_QUERIES = {"type": "object", "properties": {"queries": {"type": "array", "items": {"type": "string"}}},
                  "required": ["queries"]}


def _readable(url):
    """A page address the article reader can use (Reddit's old layout keeps posts and comments as plain HTML)."""
    p = urllib.parse.urlparse(url)
    if p.netloc.endswith("reddit.com"):
        return urllib.parse.urlunparse(p._replace(netloc="old.reddit.com"))
    return url


def find_sources(topic):
    """Search the web for the topic and read the best pages: [(site name, url, text), ...]."""
    r = _json(ask_claude(RESEARCH_QUERIES_PROMPT.format(topic=topic), schema=SCHEMA_QUERIES), "{", "}") or {}
    queries = [str(q).strip() for q in r.get("queries", []) if str(q).strip()][:6] or [topic]
    print("Research queries: " + " | ".join(queries))
    found, seen = [], set()
    skip = config.RESEARCH.get("skip_domains", ())
    for q in queries:
        for it in web_search(q) + web_search(q, news=True)[:4]:
            u = it["url"]
            if u in seen or any(d in urllib.parse.urlparse(u).netloc for d in skip):
                continue
            seen.add(u)
            found.append(it)
    if not found:
        return []
    listing = "\n".join(f"[{i}] {it['source']} | {it['title']} | {it['summary'][:200]}" for i, it in enumerate(found))
    n = config.RESEARCH.get("max_sources", 6)
    picks = parse_picks(ask_claude(RESEARCH_PICK_PROMPT.format(topic=topic, n=n, results=listing), schema=SCHEMA_IDS))
    chosen = [found[i] for i in picks if 0 <= i < len(found)][:n + 2]  # a couple spare, in case pages fail
    sources = []
    for it in chosen:
        text = fetch_article(_readable(it["url"]), 7000)
        if len(text) >= 600:
            sources.append((it["source"], it["url"], text))
            print(f"Source: {it['source']} {it['url']} ({len(text)} characters)")
        if len(sources) >= n:
            break
    return sources


def research_topic(s, topic, feedback=""):
    """Write a "Розбираємося" long-read on the topic from web sources and send it as a draft.
    feedback: an approver's notes on an earlier version, to follow this time."""
    sources = find_sources(topic)
    if len(sources) < config.RESEARCH.get("min_sources", 2):
        print(f"Not enough sources for: {topic}")
        return False
    source = "\n\n".join(f"[{i}] {name} — {url}\n{text}" for i, (name, url, text) in enumerate(sources, 1))
    request = topic + (f"\nEDITOR'S FEEDBACK on the previous version (follow it closely): {feedback}" if feedback else "")
    keys = ("title", "teaser", "body")
    post = write_long(RESEARCH_WRITE_PROMPT.format(topic=request), keys, source=source, optional=("image_query",))
    if not post:
        print("Could not write the article")
        return False
    query = (post.get("image_query") or "").strip()
    edited = parse_post(ask_claude(EDIT_PROMPT.format(
        draft=json.dumps({k: post[k] for k in keys}, ensure_ascii=False), title=topic[:200], summary="",
        article=SOURCE_REF), source=source, schema=schema_post(keys)), keys)
    post = edited if edit_ok(post, edited) else post
    post, problems = review_post(post, keys, source, topic[:300])
    header = config.LABELS["research_header"]
    image = commons_image(query) if query else ""
    names = list(dict.fromkeys(name for name, _, _ in sources))
    page = telegraph("createPage", s, title=post["title"][:256], author_name=config.TELEGRAPH_AUTHOR,
                     author_url=config.TELEGRAPH_AUTHOR_URL,
                     content=json.dumps(telegraph_nodes(post["body"], image, "Wikimedia Commons", "", "",
                                                        sources=[(n, u) for n, u, _ in sources]), ensure_ascii=False))
    print(f"Telegraph page: {page['url']}")
    e = html.escape
    text = (f"{e(header, quote=False)}\n\n<b>{e(post['title'], quote=False)}</b>\n\n{e(post['teaser'], quote=False)}"
            f"\n\n📖 <b><a href=\"{e(page['url'], quote=True)}\">{e(config.LABELS['read_more'])} →</a></b>")
    key = "research:" + hashlib.sha1((topic + now().isoformat()).encode()).hexdigest()[:12]
    card = {"kind": "news", "title": post["title"], "tag": header.split(" ", 1)[-1],
            "queries": [*split_queries(query)]}
    ok = send_draft(s, key, text, now().isoformat(), preview_url=page["url"], kind="research",
                    note=review_note(problems), card=card, fb=fb_long(header, post, ", ".join(names)))
    if ok:
        d = s["pending"][hashlib.sha1(key.encode()).hexdigest()[:10]]
        d["telegraph_path"], d["topic"] = page["path"], topic
    return ok
