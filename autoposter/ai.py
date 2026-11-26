"""Claude: the API call (prompt caching, structured answers), the glossary and editorial notes, and the
checks around every piece of writing (copy-edit validation, the reviewer agent)."""
import html
import json
import os
import re
import sys

from community import config
from community.prompts import AUDIENCE, FIX_PROMPT, REVIEW_PROMPT, STYLE

from .core import ANTHROPIC_KEY, HERE, STATE_FILE, http


SOURCE_REF = "(the source text is at the beginning of this message)"


_usage = {"calls": 0, "input": 0, "cache_read": 0, "cache_write": 0, "output": 0}


def schema_post(keys, optional=()):
    """Tool schema for a post with these text fields."""
    return {"type": "object", "properties": {k: {"type": "string"} for k in (*keys, *optional)},
            "required": list(keys)}


SCHEMA_IDS = {"type": "object", "properties": {"ids": {"type": "array", "items": {"type": "integer"}}},
              "required": ["ids"]}


SCHEMA_REVIEW = {"type": "object", "properties": {
    "verdict": {"type": "string", "enum": ["ok", "fix"]},
    "problems": {"type": "array", "items": {"type": "string"}}}, "required": ["verdict"]}


SCHEMA_REVISED = {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}


SCHEMA_LESSONS = {"type": "object", "properties": {"report": {"type": "string"},
                                                   "lessons": {"type": "array", "items": {"type": "string"}}},
                  "required": ["report", "lessons"]}


SCHEMA_TIPS = {"type": "object", "properties": {"tips": {"type": "string"}}, "required": ["tips"]}


SCHEMA_REFERRAL = {"type": "object", "properties": {"id": {"type": ["integer", "null"]}}, "required": ["id"]}


_ITEMS = {"type": "array", "items": {"type": "object", "properties": {
    "id": {"type": "integer"}, "text": {"type": "string"}}, "required": ["id", "text"]}}


SCHEMA_DIGEST = {"type": "object", "properties": {
    "national": _ITEMS,
    "regions": {"type": "array", "items": {"type": "object", "properties": {
        "region": {"type": "string"}, "region_en": {"type": "string"}, "items": _ITEMS},
        "required": ["region", "items"]}},
    "community": _ITEMS, "today": _ITEMS}, "required": ["national"]}


def _load_glossary():
    """Read community/glossary.json (established names); an empty list if it's missing."""
    try:
        path = os.path.join(HERE, "community", "glossary.json")
        return json.load(open(path, encoding="utf-8")).get("entries", [])
    except (OSError, ValueError):
        return []


GLOSSARY = _load_glossary()


_NOTES = None


def _editorial_notes():
    """Rules the approvers accepted from the monthly review (kept in state.json)."""
    global _NOTES
    if _NOTES is None:
        try:
            _NOTES = json.load(open(STATE_FILE, encoding="utf-8")).get("editorial_notes", [])
        except (OSError, ValueError):
            _NOTES = []
    return _NOTES


def glossary_for(text):
    """The glossary entries whose English names appear in this text (ALL-CAPS names only in capitals)."""
    found = []
    for entry in GLOSSARY:
        for name in entry["en"]:
            flags = 0 if name.isupper() else re.I
            if re.search(r"(?<![\w-])" + re.escape(name) + r"s?(?![\w-])", text, flags):
                found.append(f"- {entry['en'][0]} = {entry['uk']}")
                break
    return found


def ask_claude(prompt, source=None, schema=None):
    """One Claude call. With `source`, the source text goes first as a cached block: the writer, copy editor,
    reviewer and fixer all send the same source within a minute, so later calls read it from the cache at a
    fraction of the price (prompts then refer to it with SOURCE_REF instead of repeating it)."""
    if not ANTHROPIC_KEY:
        sys.exit("ANTHROPIC_API_KEY is not set")
    # Established names for the institutions this text mentions (only the matching glossary entries)
    writes = schema not in (SCHEMA_IDS, SCHEMA_REFERRAL)  # picking stories needs no names
    names = glossary_for((source or "") + "\n" + prompt.replace(STYLE, "").replace(AUDIENCE, "")) if writes else []
    notes = _editorial_notes() if writes else []
    if notes:
        prompt += ("\n\nEDITORIAL NOTES (learned from the editors' feedback and readers; follow them):\n"
                   + "\n".join(f"- {n}" for n in notes))
    if names:
        prompt += ("\n\nGLOSSARY: use exactly these Ukrainian names on first mention (a reviewer treats any other "
                   "version as an error to fix):\n" + "\n".join(names))
    if source:
        content = [{"type": "text", "text": f"SOURCE TEXT:\n{source}", "cache_control": {"type": "ephemeral"}},
                   {"type": "text", "text": prompt}]
    else:
        content = prompt
    body = {"model": config.MODEL, "max_tokens": 12000, "messages": [{"role": "user", "content": content}]}
    if schema:  # structured answer through tool use: always well-formed JSON, no parsing guesswork
        body["tools"] = [{"name": "answer", "description": "Return the answer in this structure.",
                          "input_schema": schema}]
        body["tool_choice"] = {"type": "auto"}  # this model doesn't allow forcing a tool; the prompt asks for it
        content_last = body["messages"][0]["content"]
        note = "\n\nGive your answer by calling the `answer` tool."
        if isinstance(content_last, list):
            content_last[-1]["text"] += note
        else:
            body["messages"][0]["content"] = content_last + note
    raw = http(
        "https://api.anthropic.com/v1/messages",
        body,
        {"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01"},
        timeout=180,
    )
    resp = json.loads(raw)
    u = resp.get("usage", {})
    _usage["calls"] += 1
    for k, f in (("input", "input_tokens"), ("cache_read", "cache_read_input_tokens"),
                 ("cache_write", "cache_creation_input_tokens"), ("output", "output_tokens")):
        _usage[k] += u.get(f) or 0
    if schema:
        for b in resp.get("content", []):
            if b.get("type") == "tool_use":
                data = b.get("input", {})
                return json.dumps(data["ids"] if list(data) == ["ids"] else data, ensure_ascii=False)
        print("(no tool call in the answer; reading the text instead)")  # the text parsers still work
    return "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")


def _json(text, open_ch, close_ch):
    """The JSON value between the first open_ch and the last close_ch in a reply (None if there is none)."""
    start, end = text.find(open_ch), text.rfind(close_ch)
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start:end + 1], strict=False)
    except json.JSONDecodeError:
        return None


def parse_picks(text):
    """Story ids from a picker's answer, e.g. "[4, 17]" -> [4, 17]."""
    ids = _json(text, "[", "]") or []
    return [int(i) for i in ids if isinstance(i, (int, str)) and str(i).isdigit()]


# Latin letters that look like Cyrillic ones; models sometimes mix them into Ukrainian words
HOMOGLYPHS = str.maketrans("aceiopxyACEHIKMOPTXB", "асеіорхуАСЕНІКМОРТХВ")


# A real glitch: Cyrillic letters glued to a run of Latin letters, e.g. "машaccording"
BROKEN_WORD = re.compile(r"[а-яіїєґ][a-z]{3,}|[a-z]{3,}[а-яіїєґ]", re.I)


def fix_homoglyphs(text):
    """Replace look-alike Latin letters inside Ukrainian words with the Cyrillic ones."""
    text = re.sub(r"\b\w*[а-яіїєґ]\w*\b",
                  lambda m: m.group(0).translate(HOMOGLYPHS) if re.search(r"[a-z]", m.group(0), re.I) else m.group(0),
                  text, flags=re.I)
    # the conjunction "і" typed with a Latin "i" between Ukrainian words
    return re.sub(r"(?<=[а-яіїєґ,»)]\s)([iI])(?=\s+[а-яіїєґ«(])",
                  lambda m: "і" if m.group(1) == "i" else "І", text, flags=re.I)


def edit_ok(original, edited, min_ratio=0.7):
    """Accept the copy editor's version only if it is complete: not much shorter than the original,
    ending like a finished sentence, and without broken words (Latin letters glued to Cyrillic ones)."""
    if not edited:
        return False
    for k, v in original.items():
        if not isinstance(v, str) or k == "image_query":
            continue
        new = edited.get(k, "")
        if not isinstance(new, str) or len(new) < min_ratio * len(v):
            print(f"Copy edit rejected: '{k}' came back cut short")
            return False
        m = BROKEN_WORD.search(new)
        if m:
            print(f"Copy edit rejected: broken word in '{k}': …{new[max(0, m.start() - 20):m.end() + 20]}…")
            return False
        if k in ("body", "teaser") and not re.search(r"[.!?…»)\"]\s*$", new.strip()):
            print(f"Copy edit rejected: '{k}' doesn't end with a full sentence")
            return False
    return True


def review_post(post, keys, article, topic):
    """Reviewer agent: checks the draft against its source; fixes it once if needed and checks again.
    Returns (post, remaining problems)."""
    def review(p):
        """Ask the reviewer about one version; returns its list of problems ([] = fine)."""
        r = _json(ask_claude(REVIEW_PROMPT.format(
            topic=topic, draft=json.dumps({k: p[k] for k in keys}, ensure_ascii=False), article=SOURCE_REF),
            source=article, schema=SCHEMA_REVIEW),
            "{", "}") or {}
        return [] if r.get("verdict") == "ok" else [str(x) for x in (r.get("problems") or ["unspecified"])]

    problems = review(post)
    if not problems:
        print("Review: ok")
        return post, []
    print("Review found:", "; ".join(problems))
    fixed = parse_post(ask_claude(FIX_PROMPT.format(
        problems="\n".join(f"- {p}" for p in problems),
        draft=json.dumps({k: post[k] for k in keys}, ensure_ascii=False), article=SOURCE_REF),
        source=article, schema=schema_post(keys)), keys)
    if not fixed or not edit_ok({k: post[k] for k in keys}, fixed, min_ratio=0.3):
        print("Review: the fix came back unusable; keeping the draft and flagging it")
        return post, problems
    fixed = {**post, **{k: fixed[k] for k in keys}}
    left = review(fixed)
    print("Review after fix:", "ok" if not left else "; ".join(left))
    return fixed, left


def review_note(problems):
    """A short warning for the approvers (never published)."""
    if not problems:
        return ""
    items = "\n".join(f"• {html.escape(p)}" for p in problems[:4])
    return f"\n\n<i>⚠️ {html.escape(config.LABELS['review_warning'])}:\n{items}</i>"


def write_long(prompt, keys, tries=2, source=None, optional=()):
    """Ask Claude for a post; if it comes back cut off or garbled, ask again."""
    post = None
    for _ in range(tries):
        post = parse_post(ask_claude(prompt, source=source, schema=schema_post(keys, optional)), keys)
        if post and edit_ok({k: post[k] for k in keys}, post):
            return post
        print("Draft came back incomplete; asking again")
    return post


def parse_post(text, keys=("title", "body")):
    """A post (title, body, ...) from Claude's JSON answer, cleaned up; None if a required key is missing."""
    post = _json(text, "{", "}")
    if isinstance(post, dict):
        # The model sometimes writes line breaks as the two characters "\n" inside its answer: turn them back
        post = {k: v.replace("\\n", "\n").replace("\\t", " ") if isinstance(v, str) else v for k, v in post.items()}
        post = {k: fix_homoglyphs(v) if isinstance(v, str) and k != "image_query" else v for k, v in post.items()}
    if isinstance(post, dict) and all(post.get(k) for k in keys):
        return post
    return None


def _print_usage():
    """At exit: one log line with this run's Claude calls and tokens (to keep an eye on cost)."""
    if _usage["calls"]:
        print(f"Claude usage: {_usage['calls']} calls, input {_usage['input']}, cache write {_usage['cache_write']}, "
              f"cache read {_usage['cache_read']}, output {_usage['output']} tokens")
