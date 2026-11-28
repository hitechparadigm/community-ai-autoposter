"""Publishing destinations: Telegraph long-reads and the Facebook Page; Telegram post formatting."""
import html
import json
import re
import urllib.parse

from community import config

from .core import FB_PAGE_ID, FB_TOKEN, TELEGRAPH_TOKEN, TG_TOKEN, http, post_multipart, tg


def format_post(title, body, source, url, header=""):
    """A Telegram post (HTML): optional header line, bold headline, body, then the source link."""
    e = html.escape
    top = f"{e(header, quote=False)}\n\n" if header else ""
    return (f"{top}<b>{e(title, quote=False)}</b>\n\n{e(body, quote=False)}\n\n"
            f"🔗 {e(config.LABELS['source'])}: <a href=\"{e(url, quote=True)}\">{e(source)}</a>")


def buttons(did):
    """The ✅ Publish / ❌ Skip buttons under a draft; the button data carries the draft id."""
    return {"inline_keyboard": [[
        {"text": "✅ Publish", "callback_data": f"pub:{did}"},
        {"text": "❌ Skip", "callback_data": f"skip:{did}"},
    ]]}


def preview(url):
    """Telegram link-preview options: a large preview of this page."""
    return {"url": url, "prefer_large_media": True}


_telegraph_session = {}


def telegraph(method, s, **params):
    """Call the Telegraph API (telegra.ph) with the account key from the TELEGRAPH_TOKEN secret.
    The key is never written to state.json (the repository may be public)."""
    if method not in ("createAccount", "revokeAccessToken"):
        token = TELEGRAPH_TOKEN or _telegraph_session.get("token")
        if not token:  # no secret yet: use a temporary account for this run
            print("TELEGRAPH_TOKEN is not set: using a temporary Telegraph account")
            acc = telegraph("createAccount", s, short_name=config.BOT_NAME[:32], author_name=config.TELEGRAPH_AUTHOR,
                            author_url=config.TELEGRAPH_AUTHOR_URL)
            token = _telegraph_session["token"] = acc["access_token"]
        params["access_token"] = token
    resp = json.loads(http(f"https://api.telegra.ph/{method}", params))
    if not resp.get("ok"):
        raise RuntimeError(f"Telegraph {method} failed: {resp.get('error')}")
    return resp["result"]


def telegraph_nodes(body, image, image_credit, source_name, url, sources=None):
    """Turn the article text into Telegraph content: photo, paragraphs, subheadings, source.
    sources: [(name, url), ...] for an article written from several sources (listed at the end instead)."""
    nodes = []
    figure = {"tag": "figure", "children": [{"tag": "img", "attrs": {"src": image}},
                                            {"tag": "figcaption", "children": [f"{config.LABELS['photo']}: {image_credit}"]}]}
    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if block.startswith("#"):
            nodes.append({"tag": "h4", "children": [block.lstrip("# ").strip()]})
        elif block:
            nodes.append({"tag": "p", "children": [block]})
        if image and len(nodes) == 1 and nodes[0]["tag"] == "p":
            # the photo goes after the first paragraph: as the article's first block, Telegram's Instant View
            # would show it as a cover cropped to a wide strip (a portrait loses its top and bottom)
            nodes.append(figure)
    if image and figure not in nodes:  # no opening paragraph (e.g. a subheading first): photo at the top
        nodes.insert(0, figure)
    nodes.append({"tag": "hr"})
    if sources:
        nodes.append({"tag": "p", "children": [config.LABELS["sources"] + ":"]})
        nodes.append({"tag": "ol", "children": [{"tag": "li", "children": [
            {"tag": "a", "attrs": {"href": u}, "children": [n]}]} for n, u in sources]})
    else:
        nodes.append({"tag": "p", "children": [config.LABELS["source"] + ": ", {"tag": "a", "attrs": {"href": url}, "children": [source_name]}]})
    nodes.append({"tag": "p", "children": [{"tag": "a", "attrs": {"href": config.TELEGRAPH_AUTHOR_URL},
                                            "children": [config.TELEGRAPH_AUTHOR]}]})
    return nodes


def fb_long(header, post, source_name):
    """The whole long-read as one Facebook post (Facebook readers may not open Telegram or Telegraph)."""
    body = re.sub(r"^##\s*(.+)$", lambda m: "▪️ " + m.group(1).strip().upper(), post["body"], flags=re.M)
    text = f"{header}\n\n{post['title'].upper()}\n\n{post['teaser']}\n\n{body}\n\n{config.LABELS['source']}: {source_name}"
    return fb_footer(text)


def retire_telegraph(d, s):
    """A long-read that won't be published: replace its Telegraph page with a short notice."""
    if not d.get("telegraph_path"):
        return
    try:
        telegraph("editPage", s, path=d["telegraph_path"], title=config.LABELS["unpublished"],
                  content=json.dumps([{"tag": "p", "children": [config.LABELS["unpublished"] + "."]}],
                                     ensure_ascii=False))
    except Exception as e:
        print(f"Could not retire Telegraph page: {e}")


def fb_footer(text):
    """Add the FB_FOOTER line (the invitation to the Telegram channel) to a Facebook text."""
    footer = getattr(config, "FB_FOOTER", "")
    return f"{text}\n\n{footer}" if footer else text


def fb_text(text):
    """Telegram HTML -> plain text for Facebook: links keep only their words (see FB_COMMENT for why),
    the channel signature and referral lines are dropped, and the FB_FOOTER line is added."""
    text = re.sub(r'<a href="[^"]*">&#8203;</a>', "", text)  # invisible image link
    drop = [config.TELEGRAPH_AUTHOR_URL]  # the digest's channel signature line
    if not getattr(config, "FB_REFERRALS", False):
        drop += [r[1] for r in getattr(config, "REFERRALS", [])]
    text = "\n".join(l for l in text.split("\n") if not any(f'href="{html.escape(u, quote=True)}"' in l for u in drop))
    text = re.sub(r'\n*📖 <b><a href="[^"]+">[^<]*</a></b>', "", text)  # "read more" (it goes in the comment)
    text = re.sub(r'<a href="[^"]+">(.*?)</a>', lambda m: re.sub(r"<[^>]+>", "", m.group(1)), text, flags=re.S)
    text = html.unescape(re.sub(r"</?(b|i|u|s)>", "", text))
    return fb_footer(re.sub(r"\n{3,}", "\n\n", text).strip())


def fb_comment(d):
    """The first comment: the clickable links Facebook allows (the channel, a Telegraph long-read)."""
    parts = []
    if d.get("lp", {}).get("url", "").startswith("https://telegra.ph/") and getattr(config, "FB_COMMENT_READ_MORE", ""):
        parts.append(config.FB_COMMENT_READ_MORE.format(url=d["lp"]["url"]))
    if getattr(config, "FB_COMMENT", ""):
        parts.append(config.FB_COMMENT)
    return "\n\n".join(parts)


def post_to_facebook(d):
    """Publish an approved post to the Facebook Page (only if the Facebook secrets are set): the picture card
    with the full text (or the text alone if there is no card), then the first comment with the links."""
    if not (FB_PAGE_ID and FB_TOKEN):
        return None
    message = d.get("fb") or fb_text(d["text"])
    api = "https://graph.facebook.com"
    if d.get("card"):
        path = tg("getFile", file_id=d["card"])["file_path"]
        png = http(f"https://api.telegram.org/file/bot{TG_TOKEN}/{path}")
        r = post_multipart(f"{api}/{FB_PAGE_ID}/photos", {"message": message, "access_token": FB_TOKEN},
                           {"source": ("card.png", png, "image/png")})
        post_id = r.get("post_id") or r.get("id")
    else:
        r = post_multipart(f"{api}/{FB_PAGE_ID}/feed", {"message": message, "access_token": FB_TOKEN}, {})
        post_id = r.get("id")
    comment = fb_comment(d)
    if comment and post_id:
        try:
            post_multipart(f"{api}/{post_id}/comments", {"message": comment, "access_token": FB_TOKEN}, {})
        except Exception as e:  # the post is out; a missing comment isn't worth failing over
            print(f"Facebook comment failed: {e}")
    return post_id or "ok"


def fb_stats(post_id):
    """Reactions, comments (with text) and shares of a Facebook post."""
    q = urllib.parse.urlencode({"fields": "reactions.summary(total_count).limit(0),shares,"
                                          "comments.summary(total_count).limit(25){message}",
                                "access_token": FB_TOKEN})
    try:
        r = json.loads(http(f"https://graph.facebook.com/{post_id}?{q}"))
    except Exception as e:
        print(f"Facebook stats failed for {post_id}: {str(e)[:120]}")
        return {}
    return {"reactions": r.get("reactions", {}).get("summary", {}).get("total_count", 0),
            "shares": r.get("shares", {}).get("count", 0),
            "comments": r.get("comments", {}).get("summary", {}).get("total_count", 0),
            "comment_texts": [c.get("message", "")[:300] for c in r.get("comments", {}).get("data", [])
                              if c.get("message")]}


def move_photo_down(path, s):
    """On a published Telegraph page, move a photo that opens the article to after the first paragraph, so
    Instant View shows it whole instead of as a cropped cover. The link stays the same."""
    page = telegraph("getPage", s, path=path, return_content=True)
    content = page.get("content") or []
    if not content or not isinstance(content[0], dict) or content[0].get("tag") != "figure":
        print("The page doesn't open with a photo; nothing to move")
        return False
    first_p = next((i for i, n in enumerate(content) if isinstance(n, dict) and n.get("tag") == "p"), None)
    if first_p is None:
        return False
    figure = content.pop(0)
    content.insert(first_p, figure)  # first_p was counted with the figure still in place: now right after it
    telegraph("editPage", s, path=path, title=page["title"], author_name=page.get("author_name", ""),
              author_url=page.get("author_url", ""), content=json.dumps(content, ensure_ascii=False))
    print(f"Photo moved below the first paragraph: {page['url']}")
    return True
