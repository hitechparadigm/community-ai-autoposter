"""The evaluation set: writes posts from fixed test stories (evals/cases.json) with the same code the bot uses for
real drafts, scores them with automatic checks and an independent Claude judge, and saves a scorecard.

Run it after changing prompts, the glossary or the model, and compare with the previous run:
    python3 bot.py eval            all cases
    python3 bot.py eval ID [ID]    only these cases
Results: evals/results/latest.md (readable) and latest.json, and one line per run in evals/results/history.csv.
"""
import csv
import hashlib
import json
import os
import re

from community import config
from community.prompts import JUDGE_PROMPT

from .core import HERE, now
from .ai import BROKEN_WORD, GLOSSARY, _json, _usage, ask_claude
from .news import write_news

EVAL_DIR = os.path.join(HERE, "evals")
SCHEMA_JUDGE = {"type": "object", "properties": {
    "accuracy": {"type": "integer"}, "language": {"type": "integer"}, "usefulness": {"type": "integer"},
    "notes": {"type": "string"}}, "required": ["accuracy", "language", "usefulness"]}
CHECKS = ("facts", "glossary", "people", "names_kept", "language", "form", "reviewer")
JUDGED = ("accuracy", "language", "usefulness")


def normalize(text):
    """Lower-case text with numbers written one way: no thousands separators, a decimal comma, plain spaces."""
    text = re.sub(r"[   ]", " ", text)
    text = re.sub(r"(?<=\d)[ ,](?=\d{3}\b)", "", text)      # 40 000 / 40,000 -> 40000
    text = re.sub(r"(?<=\d)\.(?=\d)", ",", text)            # 16.50 -> 16,50
    return text.replace("’", "'").lower()


def name_pattern(form):
    """A regular expression that finds a glossary name in any grammatical case: each word is matched by its stem
    (Канадська королівська кінна поліція also finds Канадської королівської кінної поліції)."""
    form = re.sub(r"\([^)]*\)", "", form.split(";")[0]).strip()
    words = [w for w in re.findall(r"[\w'’-]+", normalize(form)) if w not in ("і", "й", "та")]
    stems = [re.escape(w if len(w) <= 4 or not re.search(r"[а-яіїєґ]", w) else w[:max(4, len(w) - 4)])
             for w in words]
    # between words: spaces or a comma, and at most one short word (і / та / й)
    return r"[\s,]+(?:\S{1,2}[\s,]+)?".join(s + r"[\w'’-]*" for s in stems)


def score(case, post):
    """Automatic checks of one post. Returns {check: (passed, detail)}; detail says what failed."""
    exp, ev = case.get("expect", {}), config.EVAL
    text = f"{post['title']}\n{post['body']}"
    norm = normalize(text)
    res = {}
    missing = [f[0] for f in exp.get("facts", []) if not any(re.search(normalize(a), norm) for a in f)]
    res["facts"] = (not missing, "missing: " + ", ".join(missing) if missing else "")
    expected = [e["uk"] for e in GLOSSARY
                if any(re.search(r"(?<![\w-])" + re.escape(n) + r"s?(?![\w-])", case["title"] + "\n" + case["article"],
                                 0 if n.isupper() else re.I) for n in e["en"])]
    wrong = [u.split(";")[0] for u in expected if not re.search(name_pattern(u), norm)]
    res["glossary"] = (not wrong, "not used: " + ", ".join(wrong) if wrong else "")
    no_original = [p for p in exp.get("people", []) if not re.search(r"\([^)]*" + re.escape(p) + r"[^)]*\)", text)]
    res["people"] = (not no_original, "no original name in brackets: " + ", ".join(no_original) if no_original else "")
    lost = [k for k in exp.get("keep", []) if normalize(k) not in norm]
    bad = [a for a in exp.get("avoid", []) if normalize(a) in norm]
    res["names_kept"] = (not lost and not bad, "; ".join(
        x for x in ("translated: " + ", ".join(lost) if lost else "", "wrong form: " + ", ".join(bad) if bad else "") if x))
    found = [w for w in ev["forbidden"] if re.search(r"(?<![\w'’])" + re.escape(w), norm)]
    letters = re.findall(ev["foreign_letters"], text)
    res["language"] = (not found and not letters, ", ".join(found + sorted(set(letters))))
    low, high = ev["body_chars"].get(case["mode"], ev["body_chars"]["news"])
    form = []
    if len(re.sub(r"^\W+", "", post["title"]).split()) > ev["title_max_words"]:
        form.append("title too long")
    if not low <= len(post["body"]) <= high:
        form.append(f"body {len(post['body'])} characters (expected {low}-{high})")
    if "\\n" in text or re.search(r"https?://", text):
        form.append("literal \\n or a link in the text")
    if BROKEN_WORD.search(text):
        form.append("broken word: " + BROKEN_WORD.search(text).group(0))
    if not re.search(r"[.!?…»)\"]\s*$", post["body"].strip()):
        form.append("ends mid-sentence")
    res["form"] = (not form, "; ".join(form))
    res["reviewer"] = (not post.get("problems"), "; ".join(post.get("problems") or []))
    return res


def judge(case, post):
    """An independent Claude call grades the post against the source (1-5 per criterion, with notes)."""
    r = _json(ask_claude(JUDGE_PROMPT.format(post=f"{post['title']}\n\n{post['body']}"),
                         source=f"{case['title']}\n\n{case['article']}", schema=SCHEMA_JUDGE), "{", "}") or {}
    return {k: int(r.get(k) or 0) for k in JUDGED} | {"notes": str(r.get("notes", "")).strip()}


def cost(usage):
    """US dollars for the tokens used (prices from config.PRICES)."""
    p = getattr(config, "PRICES", {})
    return sum(usage.get(k, 0) * p.get(k, 0) for k in ("input", "cache_write", "cache_read", "output")) / 1e6


def fingerprint():
    """A short hash of the prompts and glossary, so each result can be matched with the version that produced it."""
    h = hashlib.sha1()
    for name in ("prompts.py", "glossary.json"):
        with open(os.path.join(HERE, "community", name), "rb") as f:
            h.update(f.read())
    return h.hexdigest()[:8]


def summarize(results):
    """Pass rates per check and average judge scores, from a list of case results."""
    ok = [r for r in results if r.get("post")]
    rates = {c: sum(r["checks"][c][0] for r in ok) / len(ok) if ok else 0 for c in CHECKS}
    judged = {k: sum(r["judge"][k] for r in ok) / len(ok) if ok else 0 for k in JUDGED}
    all_pass = sum(all(v[0] for v in r["checks"].values()) and
                   min(r["judge"][k] for k in JUDGED) >= config.EVAL["judge_pass"] for r in ok)
    return {"cases": len(results), "written": len(ok), "all_pass": all_pass, "check_rates": rates, "judge": judged}


def report(results, summary, meta):
    """The scorecard as Markdown."""
    mark = lambda ok: "✅" if ok else "❌"
    lines = [f"# Evaluation results", "",
             f"{meta['date']} · model `{meta['model']}` · prompts `{meta['prompts']}` · "
             f"{summary['written']}/{summary['cases']} posts written · "
             f"**{summary['all_pass']}/{summary['cases']} passed every check** · "
             f"{meta['calls']} Claude calls · ${meta['cost']:.2f} (${meta['cost_per_post']:.3f} per post)", "",
             "| Check | Pass rate |", "| --- | --- |"]
    lines += [f"| {c} | {summary['check_rates'][c]:.0%} |" for c in CHECKS]
    lines += ["", "| Judge (1-5) | Average |", "| --- | --- |"]
    lines += [f"| {k} | {summary['judge'][k]:.2f} |" for k in JUDGED]
    lines += ["", "## Cases", "", "| Case | " + " | ".join(CHECKS) + " | Judge (acc/lang/use) |",
              "| --- " * (len(CHECKS) + 2) + "|"]
    for r in results:
        if not r.get("post"):
            lines.append(f"| {r['id']} | could not write the post |" + " |" * len(CHECKS))
            continue
        j = r["judge"]
        lines.append(f"| {r['id']} | " + " | ".join(mark(r["checks"][c][0]) for c in CHECKS)
                     + f" | {j['accuracy']}/{j['language']}/{j['usefulness']} |")
    lines += ["", "## Details", ""]
    for r in results:
        if not r.get("post"):
            continue
        fails = [f"{c}: {d}" for c, (ok, d) in r["checks"].items() if not ok]
        lines += [f"### {r['id']}", "", f"**{r['post']['title']}**", "", r["post"]["body"], ""]
        if fails:
            lines += ["Failed checks: " + "; ".join(fails), ""]
        if r["judge"].get("notes"):
            lines += [f"Judge: {r['judge']['notes']}", ""]
    return "\n".join(lines) + "\n"


def cmd_eval(ids=()):
    """Run the evaluation set (or the cases with these ids) and save the scorecard."""
    with open(os.path.join(EVAL_DIR, "cases.json"), encoding="utf-8") as f:
        cases = json.load(f)["cases"]
    cases = [c for c in cases if not ids or c["id"] in ids]
    results = []
    for case in cases:
        print(f"── {case['id']}")
        item = {"title": case["title"], "summary": case["summary"], "source": case["source"],
                "url": "", "region": case["region"]}
        post = write_news(item, case["article"], case["mode"])
        if not post:
            results.append({"id": case["id"], "post": None})
            continue
        checks, verdict = score(case, post), judge(case, post)
        results.append({"id": case["id"], "post": {"title": post["title"], "body": post["body"]},
                        "checks": checks, "judge": verdict})
        print("   " + " ".join(f"{c}:{'ok' if ok else 'FAIL'}" for c, (ok, _) in checks.items())
              + f" judge {verdict['accuracy']}/{verdict['language']}/{verdict['usefulness']}")
    summary = summarize(results)
    spent = cost(_usage)
    meta = {"date": now().strftime("%Y-%m-%d"), "model": config.MODEL, "prompts": fingerprint(),
            "calls": _usage["calls"], "cost": spent, "cost_per_post": spent / max(1, summary["written"])}
    out = os.path.join(EVAL_DIR, "results")
    os.makedirs(out, exist_ok=True)
    md = report(results, summary, meta)
    with open(os.path.join(out, "latest.md"), "w", encoding="utf-8") as f:
        f.write(md)
    with open(os.path.join(out, "latest.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "summary": summary, "results": results}, f, ensure_ascii=False, indent=1)
    if not ids:  # only full runs go into the history, so the lines are comparable
        path = os.path.join(out, "history.csv")
        new = not os.path.exists(path)
        with open(path, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["date", "model", "prompts", "cases", "all_pass", *CHECKS, *JUDGED, "cost_usd"])
            w.writerow([meta["date"], meta["model"], meta["prompts"], summary["cases"], summary["all_pass"],
                        *(f"{summary['check_rates'][c]:.2f}" for c in CHECKS),
                        *(f"{summary['judge'][k]:.2f}" for k in JUDGED), f"{spent:.2f}"])
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:  # shown on the workflow run's page
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(md.split("## Details")[0])
    print(f"\n{summary['all_pass']}/{summary['cases']} passed every check; ${spent:.2f}")
