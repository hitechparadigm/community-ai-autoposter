"""Unit tests (standard library only): python -m unittest discover -s tests"""
import hashlib
import json
import os
import sys
import unittest
from datetime import datetime, timezone
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autoposter import ai, approval, cards, channels, core, drafts, sources  # noqa: E402
from community import config  # noqa: E402


class StateMerge(unittest.TestCase):
    def test_merge_keeps_both_runs_changes(self):
        base = {"pending": {"a": {"x": 1}}, "seen": {"u1": "t"}, "tg_offset": 5, "learn": []}
        ours = {"pending": {"b": {"x": 2}}, "seen": {"u1": "t", "u2": "t"}, "tg_offset": 7,   # published a, added b
                "learn": [{"t": "1", "event": "published"}], "published_log": {"2026-11-25": {"news": 2}}}
        theirs = {"pending": {"a": {"x": 1}, "c": {"x": 3}}, "seen": {"u1": "t", "u3": "t"}, "tg_offset": 6,
                  "learn": [{"t": "2", "event": "skipped"}], "published_log": {"2026-11-25": {"news": 1}}}
        out = core.merge_state(base, ours, theirs)
        self.assertEqual(set(out["pending"]), {"b", "c"})
        self.assertEqual(set(out["seen"]), {"u1", "u2", "u3"})
        self.assertEqual(out["tg_offset"], 7)
        self.assertEqual(len(out["learn"]), 2)
        self.assertEqual(out["published_log"]["2026-11-25"]["news"], 2)

    def test_visible_length_ignores_tags(self):
        self.assertEqual(core.visible_length('<b>Hi</b> <a href="https://x.ca">there</a>'), 8)


class Feeds(unittest.TestCase):
    RSS = b"""<rss><channel>
      <item><title>Story A</title><link>https://www.cbc.ca/news/a</link><description>Sum</description>
            <pubDate>Tue, 24 Nov 2026 10:00:00 GMT</pubDate></item>
      <item><title>Bing</title>
            <link>https://www.bing.com/news/apiclick.aspx?ref=FexRss&amp;url=https%3a%2f%2fglobalnews.ca%2fnews%2f1%2fx%2f&amp;c=1</link>
            <description>d</description><pubDate>Tue, 24 Nov 2026 11:00:00 GMT</pubDate></item>
    </channel></rss>"""

    def test_parse_feed_and_unwrap_search_links(self):
        items = sources.parse_feed(self.RSS, "Feed")
        self.assertEqual(items[0]["url"], "https://www.cbc.ca/news/a")
        self.assertEqual(items[0]["published"], datetime(2026, 11, 24, 10, tzinfo=timezone.utc))
        self.assertEqual(items[1]["url"], "https://globalnews.ca/news/1/x/")
        self.assertEqual(items[1]["source"], "Global News")

    def test_split_queries(self):
        self.assertEqual(sources.split_queries("A | B |  | C"), ["A", "B", "C"])

    def test_wiki_thumb(self):
        url = "https://upload.wikimedia.org/wikipedia/commons/5/5e/Manitoba_Legislative_Building.jpg?utm=1"
        self.assertTrue(sources.wiki_thumb(url).endswith("/1280px-Manitoba_Legislative_Building.jpg"))


class Writing(unittest.TestCase):
    def test_parse_post_restores_line_breaks(self):
        post = ai.parse_post(json.dumps({"title": "T", "body": "a.\\n\\n## H\\n\\nb."}))
        self.assertEqual(post["body"], "a.\n\n## H\n\nb.")

    def test_homoglyphs_fixed_inside_ukrainian_words(self):
        self.assertEqual(ai.fix_homoglyphs("мaшина"), "машина")  # Latin a inside a Cyrillic word

    def test_edit_ok_rejects_cut_short_and_broken_words(self):
        orig = {"title": "Заголовок", "body": "Перше речення тут. Друге речення тут. Третє речення тут."}
        self.assertTrue(ai.edit_ok(orig, dict(orig)))
        self.assertFalse(ai.edit_ok(orig, {"title": "Заголовок", "body": "Перше."}))
        self.assertFalse(ai.edit_ok(orig, {"title": "Заголовок", "body": orig["body"].replace("Друге", "Другеaccording")}))

    def test_edit_ok_allows_french_quotes(self):
        orig = {"title": "T", "body": "Студенти кажуть «de résistance pour l'unité étudiante» на зборах."}
        self.assertTrue(ai.edit_ok(orig, dict(orig)))

    def test_glossary_matches_names_and_capital_abbreviations_only(self):
        found = ai.glossary_for("The Canadian Security Intelligence Service and the CRA. A sin of pride.")
        self.assertTrue(any("CSIS" in f for f in found))
        self.assertTrue(any("CRA" in f for f in found))
        self.assertFalse(any("SIN" in f for f in found))


class Facebook(unittest.TestCase):
    def test_fb_text_drops_links_and_referrals_and_adds_footer(self):
        ref = config.REFERRALS[0]
        text = (f'<b>Title</b>\n\nBody\n\n🔗 Джерело: <a href="https://www.cbc.ca/x">CBC</a>\n\n'
                f'<a href="{ref[1]}">{ref[0]}</a>')
        out = channels.fb_text(text)
        self.assertNotIn("http", out.replace(config.FB_FOOTER, ""))
        self.assertIn("Джерело: CBC", out)
        self.assertNotIn(ref[0], out)
        self.assertTrue(out.endswith(config.FB_FOOTER))

    def test_fb_comment_links_long_reads(self):
        d = {"lp": {"url": "https://telegra.ph/Page-11-25"}}
        self.assertIn("https://telegra.ph/Page-11-25", channels.fb_comment(d))


class Cards(unittest.TestCase):
    def test_card_photo_skips_maps_and_outlets(self):
        self.assertEqual(cards.card_photo("https://upload.wikimedia.org/wikipedia/commons/3/38/Census_map.png"), "")
        self.assertEqual(cards.card_photo("https://i.cbc.ca/photo.jpg"), "")
        good = "https://upload.wikimedia.org/wikipedia/commons/5/5e/Manitoba_Legislative_Building.jpg"
        self.assertEqual(cards.card_photo(good), good)


class Drafts(unittest.TestCase):
    def test_daily_count_and_note(self):
        s = {}
        drafts.daily_count(s, "news", add=5)
        self.assertEqual(drafts.daily_count(s, "news"), (5, 5))
        self.assertIn("⚠️", drafts.count_note(s, "news"))

    def test_learn_keeps_title(self):
        s = {}
        drafts.learn(s, "skipped", {"text": "<b>🛂 Заголовок</b>\n\nТекст", "kind": "news"})
        self.assertEqual(s["learn"][0]["title"], "🛂 Заголовок")


class Approvals(unittest.TestCase):
    def setUp(self):
        self.calls, self.said = [], []
        patches = [
            mock.patch.object(approval, "ADMIN_IDS", ["1"]),
            mock.patch.object(approval, "tg", lambda m, **k: self.said.append(k.get("text", "")) or {"message_id": 1}),
            mock.patch.object(approval, "page_title", lambda u: "A title"),
            mock.patch.object(approval, "_draft_item",
                              lambda s, it, stamp, mode, idea="": self.calls.append((it["url"], mode, idea)) or True),
            mock.patch.object(approval, "_history_from",
                              lambda s, src, thisday, idea="": self.calls.append((src, "history", idea)) or True),
            mock.patch.object(approval, "ask_claude", lambda *a, **k: "Banff National Park"),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def send(self, text, reply=None):
        msg = {"from": {"id": 1, "first_name": "D"}, "text": text, "message_id": 7, "chat": {"type": "private"}}
        if reply:
            msg["reply_to_message"] = reply
        approval.handle_feedback(msg, {"seen": {}, "pending": {}})

    def test_link_becomes_news_draft_with_instructions(self):
        self.send("https://globalnews.ca/news/1/x/ зроби акцент на українцях")
        self.assertEqual(self.calls, [("https://globalnews.ca/news/1/x/", "news", "зроби акцент на українцях")])

    def test_history_topic_becomes_long_read(self):
        self.send("історія Банф")
        self.assertEqual(self.calls, [("wiki:Banff_National_Park", "history", "Банф")])

    def test_too_short_topic_asks_for_more(self):
        self.send("просто ідея")
        self.assertEqual(self.calls, [])
        self.assertEqual(self.said, [config.LABELS["idea_needs_link"]])

    def test_topic_without_link_becomes_research_article(self):
        with mock.patch.object(approval, "research_topic",
                               lambda s, topic, feedback="": self.calls.append((topic, "research")) or True):
            self.send("Напиши статтю про comprehensive security check для українців з CUAET")
        self.assertEqual(self.calls, [("Напиши статтю про comprehensive security check для українців з CUAET",
                                       "research")])

    def test_strangers_are_ignored(self):
        approval.handle_feedback({"from": {"id": 99}, "text": "https://x.ca", "message_id": 1}, {"pending": {}})
        self.assertEqual(self.calls, [])


class PublishFallbacks(unittest.TestCase):
    """A reply "publish" or a 👍 reaction on a draft (or its card) publishes it, like the ✅ button."""

    def setUp(self):
        self.decided = []
        key = core.admin_key("1")
        self.s = {"pending": {"abc": {"url": "u", "msgs": [[key, 10]], "card_msgs": [[key, 11]]}}, "seen": {}}
        for p in (mock.patch.object(approval, "ADMIN_IDS", ["1"]),
                  mock.patch.object(approval, "tg", lambda m, **k: {"message_id": 1}),
                  mock.patch.object(approval, "decide", lambda s, did, d, action, who:
                                    self.decided.append((did, action)) or "")):
            p.start()
            self.addCleanup(p.stop)

    def reply(self, text, to=10, sender=1):
        approval.handle_feedback({"from": {"id": sender, "first_name": "D"}, "text": text, "message_id": 7,
                                  "reply_to_message": {"message_id": to}}, self.s)

    def test_reply_publish_or_skip(self):
        self.reply("Publish!")
        self.reply("опублікуй", to=11)  # a reply to the card works too
        self.reply("❌")
        self.assertEqual(self.decided, [("abc", "pub"), ("abc", "pub"), ("abc", "skip")])

    def test_thumbs_up_publishes_other_reactions_dont(self):
        r = lambda emoji, mid=10, uid=1: {"user": {"id": uid}, "message_id": mid, "old_reaction": [],
                                         "new_reaction": [{"type": "emoji", "emoji": emoji}]}
        approval.handle_reaction(r("❤"), self.s)
        approval.handle_reaction(r("👍", uid=99), self.s)  # not an approver
        approval.handle_reaction(r("👍", mid=11), self.s)
        self.assertEqual(self.decided, [("abc", "pub")])


class Research(unittest.TestCase):
    """A topic without a link: search, pick, read, write a Telegraph article with its sources."""

    def test_article_from_web_sources(self):
        from autoposter import research
        post = {"title": "Перевірка безпеки", "teaser": "Що перевіряють.", "body": "## Як це працює\n\nТекст.",
                "image_query": ""}
        answers = iter(['{"queries": ["security screening Canada", "CUAET PR reddit"]}', "[0, 1]",
                        '{"enough": true}',
                        json.dumps({k: post[k] for k in ("title", "teaser", "body")}, ensure_ascii=False)])
        results = [{"url": "https://www.canada.ca/a", "title": "A", "summary": "", "source": "canada.ca"},
                   {"url": "https://www.facebook.com/x", "title": "F", "summary": "", "source": "facebook.com"},
                   {"url": "https://www.reddit.com/r/x/1", "title": "R", "summary": "", "source": "reddit.com"}]
        sent, read = [], []
        s = {"pending": {}}

        def send(s_, key, text, stamp, **k):
            sent.append((key, text, k))
            s_["pending"][hashlib.sha1(key.encode()).hexdigest()[:10]] = {}
            return True

        with mock.patch.object(research, "ask_claude", lambda *a, **k: next(answers)), \
                mock.patch.object(research, "claude_search", lambda *a, **k: ("", [])), \
                mock.patch.object(research, "claude_fetch", lambda urls: {}), \
                mock.patch.object(research, "web_search", lambda q, news=False: [] if news else results), \
                mock.patch.object(research, "fetch_article", lambda u, limit=0: read.append(u) or "текст " * 200), \
                mock.patch.object(research, "write_long", lambda *a, **k: dict(post)), \
                mock.patch.object(research, "review_post", lambda p, keys, src, topic, note="": (p, [])), \
                mock.patch.object(research, "telegraph", lambda *a, **k: {"url": "https://telegra.ph/x", "path": "x"}), \
                mock.patch.object(research, "commons_image", lambda q: ""), \
                mock.patch.object(research, "send_draft", send), \
                mock.patch.dict(config.RESEARCH, {"min_sources": 2}):
            self.assertTrue(research.research_topic(s, "comprehensive security check для CUAET"))
        self.assertEqual(read, ["https://www.canada.ca/a", "https://old.reddit.com/r/x/1"])  # Facebook skipped
        key, text, extra = sent[0]
        self.assertEqual(extra["kind"], "research")
        self.assertIn("telegra.ph/x", text)
        self.assertEqual(list(s["pending"].values())[0]["topic"], "comprehensive security check для CUAET")

    def test_off_topic_sources_stop_before_writing(self):
        from autoposter import research
        answers = iter(['{"queries": ["q"]}', "[0]", '{"enough": false, "missing": "Немає даних", "queries": ["q2"]}',
                        "[0]", '{"enough": false, "missing": "Немає даних про перевірку", "queries": []}'])
        pages = iter([[{"url": "https://a.ca/1", "title": "A", "summary": "", "source": "a.ca"}],
                      [{"url": "https://b.ca/2", "title": "B", "summary": "", "source": "b.ca"}]])
        with mock.patch.object(research, "ask_claude", lambda *a, **k: next(answers)), \
                mock.patch.object(research, "claude_search", lambda *a, **k: ("", [])), \
                mock.patch.object(research, "claude_fetch", lambda urls: {}), \
                mock.patch.object(research, "web_search", lambda q, news=False: [] if news else next(pages)), \
                mock.patch.object(research, "fetch_article", lambda u, limit=0: "текст " * 200), \
                mock.patch.object(research, "write_long", lambda *a, **k: self.fail("must not write")):
            with self.assertRaises(research.NotCovered) as e:
                research.research_topic({"pending": {}}, "тема")
        self.assertEqual(str(e.exception), "Немає даних про перевірку")


class ResearchWithClaudeSearch(unittest.TestCase):
    def test_pages_claude_lists_are_read_in_order(self):
        from autoposter import research
        text = ("https://www.canada.ca/en/security-screening.html — how screening works\n"
                "https://www.facebook.com/group/1 — a group\nhttps://www.reddit.com/r/ImmigrationCanada/2 — stories")
        read = []
        with mock.patch.object(research, "claude_search", lambda *a, **k: (text, [])), \
                mock.patch.object(research, "claude_fetch", lambda urls: {}), \
                mock.patch.object(research, "fetch_article", lambda u, limit=0: read.append(u) or "текст " * 200), \
                mock.patch.object(research, "ask_claude", lambda *a, **k: '{"enough": true}'):
            sources, missing = research.find_sources("тема")
        self.assertEqual(read, ["https://www.canada.ca/en/security-screening.html",
                                "https://old.reddit.com/r/ImmigrationCanada/2"])
        self.assertEqual((len(sources), missing), (2, ""))

    def test_unreadable_pages_go_through_claude_fetch(self):
        from autoposter import research
        found = [{"url": "https://a.ca/1", "source": "a.ca"}, {"url": "https://b.ca/2.pdf", "source": "b.ca"}]
        asked = []
        with mock.patch.object(research, "fetch_article", lambda u, limit=0: "" if "b.ca" in u else "текст " * 200), \
                mock.patch.object(research, "claude_fetch",
                                  lambda urls: asked.append(urls) or {"https://b.ca/2.pdf": "документ " * 100}):
            out = research._read_pages(found, 6)
        self.assertEqual(asked, [["https://b.ca/2.pdf"]])
        self.assertEqual([u for _, u, _ in out], ["https://a.ca/1", "https://b.ca/2.pdf"])


class Reviewer(unittest.TestCase):
    def test_second_round_fixes_what_the_first_missed(self):
        verdicts = iter(['{"verdict": "fix", "problems": ["a"]}', '{"verdict": "fix", "problems": ["b"]}',
                         '{"verdict": "ok"}'])
        fixes = iter(['{"title": "Заголовок один", "body": "Текст перший, повний."}',
                      '{"title": "Заголовок два", "body": "Текст другий, повний."}'])
        def fake(prompt, source=None, schema=None, fast=False):
            return next(verdicts) if schema is ai.SCHEMA_REVIEW else next(fixes)
        with mock.patch.object(ai, "ask_claude", fake):
            post, left = ai.review_post({"title": "Заголовок", "body": "Текст нульовий, повний."},
                                        ("title", "body"), "source", "topic")
        self.assertEqual((post["title"], left), ("Заголовок два", []))


class StoryRegion(unittest.TestCase):
    def test_card_tag_follows_the_story_not_the_feed(self):
        from autoposter import news
        sent = []
        item = {"url": "https://www.ctvnews.ca/regina/x", "title": "Supreme Court upholds Quebec law",
                "summary": "", "source": "CTV News Regina", "region": "Saskatchewan"}
        post = {"title": "Заголовок", "body": "Текст.", "emoji": "⚖️", "photo_query": "", "region": "Quebec",
                "problems": []}
        with mock.patch.object(news, "write_news", lambda *a, **k: dict(post)), \
                mock.patch.object(news, "fetch_article", lambda u: ""), \
                mock.patch.object(news, "matching_referral", lambda s, p: None), \
                mock.patch.object(news, "send_draft", lambda *a, **k: sent.append(k["card"]) or True):
            news._draft_item({"pending": {}}, item, "t")
        self.assertEqual(sent[0]["tag"], "Квебек")
        self.assertIn("Parliament Building (Quebec)", sent[0]["queries"])


class Models(unittest.TestCase):
    def test_simple_choices_use_the_fast_model_and_costs_are_counted(self):
        sent = []
        reply = {"content": [{"type": "text", "text": "ok"}], "usage": {"input_tokens": 1000, "output_tokens": 100}}
        with mock.patch.object(ai, "http", lambda url, body, *a, **k: sent.append(body["model"]) or json.dumps(reply)), \
                mock.patch.object(ai, "ANTHROPIC_KEY", "x"), mock.patch.dict(ai._usage, {"cost": 0.0}):
            ai.ask_claude("pick", fast=True)
            ai.ask_claude("write")
            cost = ai._usage["cost"]
        self.assertEqual(sent, [config.FAST_MODEL, config.MODEL])
        fast, main = config.PRICES[config.FAST_MODEL], config.PRICES[config.MODEL]
        self.assertAlmostEqual(cost, (1000 * (fast["input"] + main["input"]) + 100 * (fast["output"] + main["output"])) / 1e6)

    def test_digest_shortlist_keeps_community_news_and_order(self):
        from autoposter import news
        items = [{"title": f"t{i}", "region": "Canada", "community": i == 7} for i in range(40)]
        with mock.patch.object(news, "ask_claude", lambda *a, **k: json.dumps(list(range(20, 40)))), \
                mock.patch.dict(config.__dict__, {"DIGEST_SHORTLIST": 25}):
            short = news._shortlist(items)
        self.assertEqual([it["title"] for it in short], ["t7"] + [f"t{i}" for i in range(20, 40)])


class CommandLine(unittest.TestCase):
    def test_unknown_command_prints_usage(self):
        from autoposter import cli
        with self.assertRaises(SystemExit) as e:
            cli.main(["bot.py", "nonsense"])
        self.assertIn("Usage", str(e.exception))




class DigestCard(unittest.TestCase):
    def test_card_lines_are_complete_sentences(self):
        from autoposter.news import card_line
        self.assertEqual(card_line({"short": "Уряд ухвалив бюджет.", "text": "[Уряд] ухвалив бюджет на 2027 рік."}),
                         "Уряд ухвалив бюджет.")
        long_first = "Оттава домовилася з Катаром про консульські послуги. " + "Деталі " * 30
        self.assertEqual(card_line({"text": long_first}), "Оттава домовилася з Катаром про консульські послуги.")
        self.assertTrue(card_line({"text": "слово " * 40}).endswith("…"))


if __name__ == "__main__":
    unittest.main()
