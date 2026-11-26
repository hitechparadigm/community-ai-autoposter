"""Unit tests (standard library only): python -m unittest discover -s tests"""
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

    def test_news_idea_without_link_asks_for_one(self):
        self.send("просто ідея")
        self.assertEqual(self.calls, [])
        self.assertEqual(self.said, [config.LABELS["idea_needs_link"]])

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
