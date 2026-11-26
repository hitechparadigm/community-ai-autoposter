"""Shared basics: settings from the environment, time, HTTP, the bot's memory (state.json), Telegram calls."""
import hashlib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from community import config


HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # the repository folder


# The bot's memory: in the private "<repository>-state" repository when the workflow checked it out into .state
# (keeps drafts and reader data out of the public repo), otherwise state.json in the repository folder.
STATE_FILE = (os.path.join(HERE, ".state", "state.json") if os.path.isdir(os.path.join(HERE, ".state", ".git"))
              else os.path.join(HERE, "state.json"))


if (STATE_FILE.endswith(os.path.join(".state", "state.json")) and not os.path.exists(STATE_FILE)
        and os.path.exists(os.path.join(HERE, "state.json"))):  # first run with the state repo: move the memory over
    import shutil
    shutil.copyfile(os.path.join(HERE, "state.json"), STATE_FILE)


UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")


# Wikimedia asks bots to identify themselves (and throttles generic browser user agents)
WIKI_UA = f"{config.BOT_NAME}/1.0 ({config.BOT_CONTACT_URL})"


ATOM = "{http://www.w3.org/2005/Atom}"


DC = "{http://purl.org/dc/elements/1.1/}"


TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")


# One or more approver IDs, comma-separated (e.g. "456360947,123456789")
ADMIN_IDS = [x.strip() for x in os.environ.get("TELEGRAM_ADMIN_ID", "").split(",") if x.strip()]


ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")


TELEGRAPH_TOKEN = os.environ.get("TELEGRAPH_TOKEN", "").strip()


FB_PAGE_ID = os.environ.get("FACEBOOK_PAGE_ID", "").strip()


FB_TOKEN = os.environ.get("FACEBOOK_PAGE_TOKEN", "").strip()


def now():
    """The current time, in UTC (convert with .astimezone(LOCAL) for local times)."""
    return datetime.now(timezone.utc)


def http(url, data=None, headers=None, timeout=30):
    """GET (or POST JSON when data is given) a URL and return the raw bytes; raises RuntimeError on HTTP errors."""
    h = {"User-Agent": WIKI_UA if re.search(r"wiki[mp]edia\.org", url) else UA}
    h.update(headers or {})
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        raise RuntimeError(f"HTTP {e.code} from {url.split('?')[0]}: {detail}") from None


def load_state():
    """The bot's memory (state.json): seen stories, drafts waiting for approval, read position, logs."""
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            s = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        s = {}
    s.setdefault("seen", {})      # url -> ISO time first seen
    s.setdefault("pending", {})   # draft id -> draft
    s.setdefault("tg_offset", 0)
    return s


def save_state(s):
    """Write the bot's memory back to state.json (save_state.sh then commits and pushes it)."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=1, sort_keys=True)


def merge_state(base, ours, theirs):
    """Three-way merge when two runs saved state at the same time.
    theirs = state already on GitHub, ours = this run's state, base = what this run started from."""
    out = json.loads(json.dumps(theirs))
    for k in ("seen", "pending"):
        out.setdefault(k, {})
    for did, d in ours.get("pending", {}).items():
        if did not in base.get("pending", {}):
            out["pending"][did] = d            # we added a draft
    for did in base.get("pending", {}):
        if did not in ours.get("pending", {}):
            out["pending"].pop(did, None)      # we published, skipped or expired it
    out["seen"].update(ours.get("seen", {}))
    done = out.get("history_done", [])
    out["history_done"] = done + [x for x in ours.get("history_done", []) if x not in done]
    out["tg_offset"] = max(theirs.get("tg_offset", 0), ours.get("tg_offset", 0))
    out["digest_regions"] = {**out.get("digest_regions", {}), **ours.get("digest_regions", {})}
    out["ref_index"] = max(theirs.get("ref_index", 0), ours.get("ref_index", 0))
    out["schedule_done"] = {**out.get("schedule_done", {}), **ours.get("schedule_done", {})}
    rn_t, rn_o = theirs.get("ref_news", {}), ours.get("ref_news", {})
    out["ref_news"] = max((rn_t, rn_o), key=lambda r: (r.get("date", ""), r.get("count", 0)))
    if ours.get("thisday_last"):
        out["thisday_last"] = ours["thisday_last"]
    # learning data: lists are combined (no duplicates), dicts updated with this run's values
    for k in ("learn", "tg_comments"):
        seen_items = {json.dumps(x, sort_keys=True) for x in out.get(k, [])}
        out[k] = out.get(k, []) + [x for x in ours.get(k, []) if json.dumps(x, sort_keys=True) not in seen_items]
    for k in ("tg_reactions", "lessons_pending", "tg_comment_count"):
        out[k] = {**out.get(k, {}), **ours.get(k, {})}
    for k in ("lessons_pending",):  # handled (removed) by this run
        for lid in base.get(k, {}):
            if lid not in ours.get(k, {}):
                out[k].pop(lid, None)
    log = out.setdefault("published_log", {})
    for day, kinds in ours.get("published_log", {}).items():
        for kind, n in kinds.items():
            log.setdefault(day, {})[kind] = max(log.get(day, {}).get(kind, 0), n)
    if len(ours.get("editorial_notes", [])) >= len(out.get("editorial_notes", [])):
        out["editorial_notes"] = ours.get("editorial_notes", [])
    out.pop("telegraph_token", None)
    return out


def tg(method, **params):
    """Call a Telegram Bot API method and return its result; raises RuntimeError if Telegram says no."""
    if not TG_TOKEN:
        sys.exit("TELEGRAM_BOT_TOKEN is not set")
    raw = http(f"https://api.telegram.org/bot{TG_TOKEN}/{method}", params)
    resp = json.loads(raw)
    if not resp.get("ok"):
        raise RuntimeError(f"Telegram {method} failed: {resp}")
    return resp["result"]


def admin_key(admin_id):
    """A short, non-reversible label for an approver, so their Telegram ID isn't stored in state.json."""
    return hashlib.sha256(f"approver:{admin_id}".encode()).hexdigest()[:10]


def multipart(fields, files):
    """Encode a multipart/form-data body. files: {name: (filename, bytes, content type)}."""
    boundary = "----autoposter" + hashlib.sha1(os.urandom(8)).hexdigest()
    out = b""
    for k, v in fields.items():
        out += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n").encode()
    for k, (fname, data, ctype) in files.items():
        out += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{fname}\"\r\n"
                f"Content-Type: {ctype}\r\n\r\n").encode() + data + b"\r\n"
    return out + f"--{boundary}--\r\n".encode(), f"multipart/form-data; boundary={boundary}"


def post_multipart(url, fields, files, timeout=60):
    """POST a form with files (used for picture uploads to Telegram and Facebook); returns the JSON reply."""
    body, ctype = multipart(fields, files)
    req = urllib.request.Request(url, data=body, headers={"Content-Type": ctype, "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(e.read().decode(errors="replace")[:300]) from None


def visible_length(text):
    """Length of a Telegram HTML message as Telegram counts it: tags removed, entities decoded."""
    return len(html.unescape(re.sub(r"<[^>]+>", "", text)))


WIKI = f"https://{config.WIKIPEDIA_LANG}.wikipedia.org"


LOCAL = ZoneInfo(config.TIMEZONE)  # for picking "today", showing times and the schedule


def answer(cq, text, alert=False):
    # Telegram rejects answers to taps older than a few minutes; that's harmless.
    """Answer an approver's button tap with a short pop-up text."""
    try:
        tg("answerCallbackQuery", callback_query_id=cq["id"], text=text, show_alert=alert)
    except Exception as e:
        print(f"(could not answer tap: {e})")
