"""Facebook picture cards, drawn from card.html with headless Chrome."""
import html
import os
import re
import urllib.parse

from community import config

from .core import ADMIN_IDS, admin_key, FB_PAGE_ID, FB_TOKEN, HERE, LOCAL, TG_TOKEN, http, now, post_multipart, tg
from .sources import commons_image, wiki_thumb


def card_photo(url):
    """Only freely licensed photos go on cards (news outlets' photos are copyrighted)."""
    if not url or not any(d in url for d in config.CARD.get("photo_domains", ("wikimedia.org",))):
        return ""
    if NOT_A_PHOTO.search(urllib.parse.unquote(url.split("?")[0].rsplit("/", 1)[-1])):  # maps, flags, charts
        return ""
    return url


NOT_A_PHOTO = re.compile(r"\.png$|\.svg|map|census|flag|coat_of_arms|seal|diagram|chart|logo|locator", re.I)


MAPLE_LEAF = ("m-90 2030 45-863a95 95 0 0 0-111-98l-859 151 116-320a65 65 0 0 0-20-73l-941-762 212-99a65 65 0 0 0 "
              "34-79l-186-572 542 115a65 65 0 0 0 73-38l105-247 423 454a65 65 0 0 0 111-57l-204-1052 327 189a65 65 "
              "0 0 0 91-27l332-652 332 652a65 65 0 0 0 91 27l327-189-204 1052a65 65 0 0 0 111 57l423-454 105 247a65 "
              "65 0 0 0 73 38l542-115-186 572a65 65 0 0 0 34 79l212 99-941 762a65 65 0 0 0-20 73l116 320-859-151a95 "
              "95 0 0 0-111 98l45 863z")  # the leaf from the Flag of Canada (public domain)


def render_card(card):
    """Draw a Facebook picture card from card.html with headless Chrome. Returns PNG bytes, or b"" if it can't."""
    import base64, shutil, subprocess, tempfile
    chrome = next((c for c in ("google-chrome", "chromium", "chromium-browser") if shutil.which(c)), None)
    tpl = os.path.join(HERE, "community", "card.html")
    if not chrome or not os.path.exists(tpl):
        print("Card skipped: Chrome or card.html not found")
        return b""
    c, e = config.CARD, html.escape
    w, h = c["size"]
    d = now().astimezone(LOCAL)
    background = credit = ""
    photo = card_photo(card.get("photo", ""))
    if photo:
        try:
            data = http(wiki_thumb(photo), timeout=40)
            mime = "image/png" if data[:4] == b"\x89PNG" else "image/jpeg"
            background = (f'<div class="photo" style="background-image:url(data:{mime};base64,'
                          f'{base64.b64encode(data).decode()})"></div>')
            who = card.get("credit") or ("Wikimedia Commons" if "wikimedia.org" in photo
                                         else urllib.parse.urlparse(photo).netloc.replace("www.", ""))
            credit = f'<div class="credit">{e(config.LABELS["photo"])}: {e(who)}</div>'
        except Exception as ex:
            print(f"Card photo failed, using the plain background: {ex}")
    kind = card.get("kind", "news")
    items = ""
    if card.get("items"):
        items = "<ol>" + "".join(f"<li>{e(i)}</li>" for i in card["items"]) + "</ol>"
    bigdate = ""
    if kind == "thisday":
        bigdate = f'<div class="bigdate">{d.day}<small>{e(config.MONTHS[d.month - 1])}</small></div>'
    tag = f'<div class="tag">{e(card["tag"])}</div>' if card.get("tag") else ""
    values = {"kind": kind, "layout": "withphoto" if background else "nophoto", "background": background, "credit": credit, "items": items, "bigdate": bigdate,
              "tag": tag, "title": e(card.get("title", "")), "brand": e(c["brand"]),
              "tagline": e(c.get("tagline", "")), "cta": e(c.get("cta", "")),
              "date": f"{d.day} {config.MONTHS[d.month - 1]} {d.year}", "handle": e(c.get("handle", "")),
              "handle2": e(c.get("handle2", "")), "width": w, "height": h, "band": c.get("band", 0),
              "band_color": c.get("band_color", "#A51D18"), **c.get("colors", {})}
    leaf = f'<path d="{MAPLE_LEAF}"/>'
    values["leaves"] = (f'<svg class="leaf-l" viewBox="-2015 -2000 4030 4030">{leaf}</svg>'
                        f'<svg class="leaf-r" viewBox="-2015 -2000 4030 4030">{leaf}</svg>') if c.get("band") else ""
    page = open(tpl, encoding="utf-8").read()
    for k, v in values.items():
        page = page.replace("{{" + k + "}}", str(v))
    with tempfile.TemporaryDirectory() as tmp:
        src, out = os.path.join(tmp, "card.html"), os.path.join(tmp, "card.png")
        open(src, "w", encoding="utf-8").write(page)
        try:
            subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", f"--window-size={w + 2 * c.get('band', 0)},{h}",
                            "--virtual-time-budget=15000", f"--screenshot={out}", src],
                           capture_output=True, timeout=90)
            return open(out, "rb").read()
        except Exception as ex:
            print(f"Card rendering failed: {ex}")
            return b""


def send_card(png, caption="Facebook", sent=None):
    """Show the card to the approvers in Telegram; Telegram also stores it until it's published.
    sent: a list that gets [approver key, message id] per copy (so a reply or 👍 on the card counts too)."""
    file_id = ""
    for admin in ADMIN_IDS:
        try:
            fields = {"chat_id": admin, "caption": caption}
            if file_id:  # already uploaded once: reuse it
                r = tg("sendPhoto", photo=file_id, **fields)
                if sent is not None:
                    sent.append([admin_key(admin), r["message_id"]])
                continue
            r = post_multipart(f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto", fields,
                               {"photo": ("card.png", png, "image/png")})
            file_id = r["result"]["photo"][-1]["file_id"]
            if sent is not None:
                sent.append([admin_key(admin), r["result"]["message_id"]])
        except Exception as ex:
            print(f"Could not send the card to approver #{ADMIN_IDS.index(admin) + 1}: {ex}")
    return file_id


def make_card(card, sent=None):
    """Render and store a card for Facebook. Only when Facebook is set up (or CARDS_ALWAYS for testing)."""
    if not card or not ((FB_PAGE_ID and FB_TOKEN) or os.environ.get("CARDS_ALWAYS")):
        return ""
    for q in card.get("queries", []):  # find a free photo only now, when the card is really made
        if card.get("photo"):
            break
        card["photo"] = card_photo(commons_image(q)) if q else ""
    png = render_card(card)
    return send_card(png, "🖼 Facebook", sent) if png else ""
