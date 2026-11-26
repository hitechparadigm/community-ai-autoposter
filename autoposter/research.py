"""Articles on a topic an approver sends without a link ("🔎 Розбираємося"): the bot searches the web, picks the
most reliable pages, reads them, and writes a long-read from them (published on Telegraph, with a teaser post
and the list of sources), checked by the same copy editor and reviewer as every other post."""
import hashlib
import html
import json
import urllib.parse

from community import config
from community.prompts import (EDIT_PROMPT, RESEARCH_COVERAGE_PROMPT, RESEARCH_PICK_PROMPT, RESEARCH_QUERIES_PROMPT,
                               RESEARCH_WRITE_PROMPT)

from .core import now
from .sources import commons_image, fetch_article, split_queries, web_search
from .ai import (SCHEMA_IDS, SOURCE_REF, _json, ask_claude, edit_ok, parse_picks, parse_post, review_note,
                 review_post, schema_post, write_long)
from .channels import fb_long, telegraph, telegraph_nodes
from .drafts import send_draft

class NotCovered(Exception):
    """The pages found don't cover the topic; the message says what is missing (for the approver)."""


SCHEMA_QUERIES = {"type": "object", "properties": {"queries": {"type": "array", "items": {"type": "string"}}},
                  "required": ["queries"]}


def _readable(url):
    """A page address the article reader can use (Reddit's old layout keeps posts and comments as plain HTML)."""
    p = urllib.parse.urlparse(url)
    if p.netloc.endswith("reddit.com"):
        return urllib.parse.urlunparse(p._replace(netloc="old.reddit.com"))
    return url


SCHEMA_COVERAGE = {"type": "object", "properties": {
    "enough": {"type": "boolean"}, "missing": {"type": "string"},
    "queries": {"type": "array", "items": {"type": "string"}}}, "required": ["enough"]}


def _search(queries, skip_urls):
    """Run web and news searches; new results only (no social networks from RESEARCH skip_domains)."""
    found = []
    skip = config.RESEARCH.get("skip_domains", ())
    for q in queries:
        web, news = web_search(q), web_search(q, news=True)[:4]
        print(f"Search '{q}': {len(web)} web, {len(news)} news results")
        for it in web + news:
            u = it["url"]
            if u in skip_urls or any(d in urllib.parse.urlparse(u).netloc for d in skip):
                continue
            skip_urls.add(u)
            found.append(it)
    return found


def _read(topic, found, n):
    """Let Claude pick the most reliable results and read those pages: [(site, url, text), ...]."""
    if not found:
        return []
    listing = "\n".join(f"[{i}] {it['source']} | {it['url'][:90]} | {it['title']} | {it['summary'][:160]}"
                        for i, it in enumerate(found))
    picks = parse_picks(ask_claude(RESEARCH_PICK_PROMPT.format(topic=topic, n=n, results=listing), schema=SCHEMA_IDS))
    out = []
    for it in [found[i] for i in picks if 0 <= i < len(found)][:n + 2]:  # a couple spare, in case pages fail
        text = fetch_article(_readable(it["url"]), 7000)
        if len(text) >= 600:
            out.append((it["source"], it["url"], text))
            print(f"Source: {it['source']} {it['url']} ({len(text)} characters)")
        if len(out) >= n:
            break
    return out


def _joined(sources):
    """All sources as one numbered text (the source block every writing step reads)."""
    return "\n\n".join(f"[{i}] {name} — {url}\n{text}" for i, (name, url, text) in enumerate(sources, 1))


def find_sources(topic):
    """Search the web for the topic and read the best pages; if they don't cover the topic, search again for
    what is missing (one more round). Returns ([(site, url, text), ...], what is still missing or "")."""
    r = _json(ask_claude(RESEARCH_QUERIES_PROMPT.format(topic=topic), schema=SCHEMA_QUERIES), "{", "}") or {}
    queries = [str(q).strip() for q in r.get("queries", []) if str(q).strip()][:6] or [topic]
    seen, n = set(), config.RESEARCH.get("max_sources", 6)
    sources = _read(topic, _search(queries, seen), n)
    missing = ""
    for _ in range(2):  # check coverage; at most one extra search round
        if not sources:
            return [], ""
        c = _json(ask_claude(RESEARCH_COVERAGE_PROMPT.format(topic=topic), source=_joined(sources),
                             schema=SCHEMA_COVERAGE), "{", "}") or {}
        if c.get("enough"):
            return sources, ""
        missing = str(c.get("missing", "")).strip()
        print(f"Sources don't cover the topic yet: {missing}")
        more = [str(q).strip() for q in c.get("queries", []) if str(q).strip()][:4]
        if not more or len(sources) >= n + 3:
            break
        sources += _read(topic, _search(more, seen), 3)
    return sources, missing


def research_topic(s, topic, feedback=""):
    """Write a "Розбираємося" long-read on the topic from web sources and send it as a draft.
    feedback: an approver's notes on an earlier version, to follow this time.
    Raises NotCovered when the sources found don't cover the topic (nothing is written then)."""
    sources, missing = find_sources(topic)
    if len(sources) < config.RESEARCH.get("min_sources", 2) or missing:
        print(f"Not enough sources for: {topic}")
        raise NotCovered(missing)
    source = _joined(sources)
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
